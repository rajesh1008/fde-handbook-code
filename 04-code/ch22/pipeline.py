"""Pennant's document pipeline as run in the shadow week (N01 to N15), with the door,
linkage, reconciliation rules and exception routing (Chapter 22 lab).

v1 is what ran on days 124 to 130: scorer pennant-qs-1.0, photo lane scored on the
vision reader's output, linkage by the first key that resolves to a booking.
v2 is the fix after the thumb (day 133): scorer pennant-qs-1.1 reads identifier zones
from the faithful OCR layer, and linkage needs two keys that agree.
"""
import _paths  # noqa: F401
from fieldkit.quality import Check, QualityScorer
from fieldkit.connectors import parse_x12, EDIError
from fieldkit.lineage import LineageStore
from checks import CHECKS          # Chapter 21's pennant-qs-1.0, unchanged
from pennant import u, container_ok
from week import KEYS, RATE_CARD_ACC, container, x12_210

ZONE_FLOOR = 0.80      # identifier zones must be read at this confidence or go to a person
DATE_FLOOR = 0.90      # N05: handwritten delivery date
R3_PCT = 0.005         # R3 tolerance: USD 1.00 or 0.5% of the contract amount, whichever is larger
QUEUES = {"sender request": "Dana Whitaker (freight audit)", "clerk read": "document clerks",
          "reconciliation": "reconciliation team", "escalation": "rule owner"}
RULE_OWNER = {"R1": "Kofi Mensah", "R2": "Dana Whitaker", "R3": "Dana Whitaker", "R4": "billing manager",
              "R5": "compliance manager", "R6": "Jenna Ruiz"}


def _zones(d):
    bad = [f"{k} zone confidence {c:.2f}" for k, c in sorted(d["zone_conf"].items())
           if d.get(k) is not None and k in KEYS.get(d["kind"], ()) and c < ZONE_FLOOR]
    return "; ".join(bad) or None


def scorer(version):
    from fieldkit.quality import QualityScorer as Q
    checks = list(CHECKS)
    if version == "pennant-qs-1.1":
        checks.append(Check("identifier zones read", "legibility", _zones))
    return Q(checks, version)


def vision_read(d, bk):
    """What the photo lane's vision reader returns. On an occluded identifier it does not
    leave a gap: it completes the number from what it can see, often the sibling container
    on the packing list photographed in the same message (the rewrite the research describes)."""
    r = dict(d)
    if "occluded" in d["_truth"]:
        sib = bk[d["_ship"]]["sibling"]
        r["container"] = bk[sib]["container"] if sib is not None else container(d["container"][:4], 500000 + d["_ship"])
    return r


def door(d, bk, version):
    """Return (decision, verdict line, the fields the rest of the pipeline sees)."""
    if d["channel"] == "edi":
        return ("request" if "envelope" in d["_truth"] else "accept"), None, dict(d)
    s = scorer(version)
    seen = vision_read(d, bk) if (d["channel"] == "photo" and version == "pennant-qs-1.0") else dict(d)
    # pennant-qs-1.1 scores the OCR layer, where the zone under a thumb reads at low confidence;
    # the vision reader runs only on photos the door has already accepted
    v = s.score(seen)
    if d["channel"] == "photo" and version == "pennant-qs-1.1" and v.decision == "accept":
        seen = vision_read(d, bk)
    return v.decision, v.line(), seen


def resolve(bk_index, key, value):
    return bk_index.get((key, value))


def index(bk):
    ix = {}
    for s, b in bk.items():
        for k in ("container", "bol_no", "booking_ref"):
            ix[(k, b[k])] = s
    return ix


def link(seen, ix, mode):
    keys = [k for k in KEYS[seen["kind"]] if seen.get(k)]
    if seen["kind"] == "freight invoice":
        keys = ["container", "bol_no", "booking_ref"]
    hits = [(k, resolve(ix, k, seen.get(k))) for k in keys]
    if mode == "first key":
        for k, s in hits:
            if s is not None:
                return s, f"linked by {k}"
        return None, "no key resolves"
    found = {s for _, s in hits if s is not None}
    if len([1 for _, s in hits if s is not None]) >= 2 and len(found) == 1:
        return found.pop(), "linked by " + " and ".join(k for k, s in hits if s is not None)
    if len(found) > 1:
        return None, "keys disagree: " + ", ".join(f"{k}->{bk_ref(s)}" for k, s in hits if s is not None)
    return None, "fewer than two keys resolve"


def bk_ref(s):
    return f"PN-{48000 + s}"


def rules(seen, b, fx, misread=False):
    """Reconciliation rules R1 to R6. Return {rule: (verdict, detail)}; verdict agree/disagree."""
    out = {}
    k = seen["kind"]
    gross = seen.get("gross_kg")
    total = seen.get("total")
    if misread and total is not None:
        total = round(total * 1.10, 2)
    elif misread and gross is not None:
        gross = round(gross * 1.10, 0)
    if k in ("bill of lading", "packing list", "freight invoice", "customs declaration") and seen.get("container"):
        out["R1"] = ("agree", "") if seen["container"] == b["container"] else ("disagree", f"{seen['container']} vs TMS {b['container']}")
    if k in ("bill of lading", "packing list", "freight invoice") and gross is not None:
        ref = b["chargeable_kg"] if k == "freight invoice" else b["gross_kg"]
        out["R2"] = ("agree", "") if abs(gross - ref) <= 0.02 * ref else ("disagree", f"{gross:,.0f} kg vs {ref:,.0f} kg")
    if k == "freight invoice" and total is not None:
        usd = round(total * fx[seen["currency"]], 2)
        gap = usd - b["contract_usd"]
        ok = abs(gap) <= max(1.00, R3_PCT * b["contract_usd"])
        out["R3"] = ("agree" if ok else "disagree", f"{seen['currency']} {total:,.2f} = USD {usd:,.2f}, contract {b['contract_usd']:,.2f}")
        extra = [a for a in seen.get("acc", []) if a not in RATE_CARD_ACC]
        out["R4"] = ("disagree", "not on rate card: " + ", ".join(extra)) if extra else ("agree", "")
    if k in ("commercial invoice", "customs declaration") and total is not None:
        usd = total * fx[seen["currency"]]
        out["R5"] = ("agree", "") if abs(usd - b["declared_value"]) <= 0.005 * b["declared_value"] else ("disagree", f"USD {usd:,.2f} vs declared {b['declared_value']:,.2f}")
    if k == "bill of lading" and seen.get("delivery_day") is not None:
        out["R6"] = ("agree", "") if abs(seen["delivery_day"] - b["delivered_day"]) <= 1 else ("disagree", f"day {seen['delivery_day']} vs 214 day {b['delivered_day']}")
    return out


def run(docs, bk, refs, fx_vid, version="pennant-qs-1.0", link_mode="first key", date_floor=DATE_FLOOR, lineage=True):
    """Run the week. Returns one result dict per document."""
    fx = refs.get(fx_vid)
    ix = index(bk)
    store = LineageStore(refs) if lineage else None
    edi_ok = _edi_parse(docs)
    res = []
    for d in docs:
        r = dict(doc_id=d["doc_id"], channel=d["channel"], kind=d["kind"], day=d["day"])
        if d["channel"] == "edi" and d["doc_id"] not in edi_ok:
            r.update(outcome="held", queue="sender request", why="X12 210 refused: SE count does not match")
            res.append(r); continue
        decision, line, seen = door(d, bk, version)
        if decision != "accept":
            r.update(outcome="held", queue="sender request", why=line)
            res.append(r); continue
        if d["channel"] != "edi" and d["layout"] == "L??":
            r.update(outcome="person", queue="clerk read", why="N03 layout not in the 41 known families")
            res.append(r); continue
        if d["kind"] == "bill of lading" and d.get("date_conf", 1.0) < date_floor:
            r.update(outcome="person", queue="clerk read", why=f"N05 handwritten date confidence {d['date_conf']:.2f}")
            res.append(r); continue
        if d["kind"] == "bill of lading" and u(d["doc_id"], "dmis") < max(0.0, 0.9 - d.get("date_conf", 1.0)) * 2.5:
            seen = dict(seen, delivery_day=seen["delivery_day"] + 4)     # a 1 read as a 7
        s, how = link(seen, ix, link_mode)
        if s is None:
            r.update(outcome="person", queue="clerk read", why="N07 " + how)
            res.append(r); continue
        r["linked"] = s
        b = bk[s]
        if (b["customs_hold"] and d["kind"] in ("customs declaration", "bill of lading")) or (b["late"] and d["kind"] == "bill of lading"):
            r.update(outcome="person", queue="escalation", why="N09 customs hold" if b["customs_hold"] else "N11 service level")
            res.append(r); continue
        rs = rules(seen, b, fx, misread=d.get("_misread", False))
        bad = {k: v for k, v in rs.items() if v[0] == "disagree"}
        r.update(rules=rs, linked_by=how)
        if bad:
            r.update(outcome="exception", queue="reconciliation", why="; ".join(f"{k} {v[1]}" for k, v in sorted(bad.items())))
        else:
            r.update(outcome="matched", queue=None, why=how)
        if store is not None:
            r["claim"] = _chain(store, d, r, version, fx_vid, b, fx)
        res.append(r)
    return res, store


def _edi_parse(docs):
    from week import x12_210
    ok = set()
    for (_car, _day), text in x12_210(docs).items():
        sets, errors = parse_x12(text)
        for segs in sets:
            ok.add(segs[1][2])        # B3 element 2 carries the document id in the stand-in
    return ok


def _chain(store, d, r, version, fx_vid, b, fx):
    src = store.add("source", uri=f"intake://{d['channel']}/{d['doc_id']}", sha256=d["_sha256"])
    page = store.add("page", [src], page=1)
    method = {"edi": "x12-210 parser", "scan": f"template zones {d['layout']}", "photo": "vision reader, photo lane"}[d["channel"]]
    ext = store.add("extraction", [page], method=method, scorer=version, pin="extract-2026-04")
    parents = [ext]
    if "R3" in r["rules"]:
        tot = d["total"]
        parents = [store.add("calculation", [ext], function="R3 freight charge in USD", refs={"fx": fx_vid},
                             currency=d["currency"], amount=tot, value=round(tot * fx[d["currency"]], 2))]
    return store.add("claim", parents, text=f"{r['outcome']} to {bk_ref(r['linked'])}", report="shadow week")


def recompute(node, store):
    rows = store.refs.get(node.attrs["refs"]["fx"])
    return node.attrs["amount"] * rows[node.attrs["currency"]]


def ruling(d, bk):
    """What Pennant's reconciliation team ruled for the document, after reading it in full."""
    if d["_truth"]:
        return "hold"
    if d.get("_disc"):
        return "discrepancy"
    return "match"


def grade(docs, bk, res):
    """Score each system outcome against the team's ruling."""
    out = []
    for d, r in zip(docs, res):
        t = ruling(d, bk)
        o = r["outcome"]
        right_ship = r.get("linked") == d["_ship"]
        if o == "matched":
            g = "matched" if (t == "match" and right_ship) else "silently wrong"
        elif o == "exception":
            g = "exception confirmed" if (t == "discrepancy" and right_ship) else "false exception"
        elif o == "held":
            g = "held, confirmed" if t == "hold" else "held, not needed"
        else:
            g = "to a person"
        out.append(g)
    return out
