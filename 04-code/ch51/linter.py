"""The engagement catalog linter. One rule per anti-pattern; each returns (status, detail).

Statuses: PASS, FLAG (the anti-pattern is present), WARN (the pattern holds with a known weakness),
DEV (a registered, owned deviation), N/A (the engagement has not reached the phase the rule needs).

`gated=False` is the v0 linter, kept so the lab can show the failure injection: v0 accepts a sponsor map
on its naive score, the share of role columns with any name, which passes a map with no operator.
"""
import _paths  # noqa: F401
from fieldkit.gates import wilson
from fieldkit.scoping import RANK
from fieldkit.playbooks import lint_engagement, Registry
import stakeholders as SH

GUARDED = {"join", "arithmetic", "threshold", "identity"}
MODEL_CLASSES = {"small model", "frontier model"}
HANDED = ("handed over", "retained duties")
ORDER = ["shadow", "live", "handed over", "retained duties", "managed service"]


def _reached(m, phase):
    return m["phase"] in ORDER and ORDER.index(m["phase"]) >= ORDER.index(phase)


def r01(m, gated=True):
    p = m.get("pilot")
    if not p:
        return "N/A", "no pilot or shadow period yet"
    if p.get("signed_before"):
        return "PASS", "exit rule signed before the shadow run began"
    if p.get("exit_rule_day") is None:
        return "FLAG", f"pilot running since day {p['start']} with no signed exit rule"
    if p["exit_rule_day"] > p["start"]:
        return "FLAG", f"exit rule signed day {p['exit_rule_day']}, after the pilot started day {p['start']}"
    return "PASS", f"exit rule day {p['exit_rule_day']}, pilot from day {p['start']}"


def r02(m, gated=True):
    sm = m.get("smap")
    if sm is None:
        return "FLAG", "no sponsor map"
    if not gated:   # v0: a slide-level check
        ok = SH.naive_score(sm) >= 0.75 and sm.holders("sponsor")
        return ("PASS" if ok else "FLAG"), f"naive score {SH.naive_score(sm):.2f}, sponsor named"
    sponsors = {p.key for p in sm.holders("sponsor")}
    ops = [p for p in sm.holders("operator") if p.key not in sponsors and p.source == "observed"]
    if not ops:
        return "FLAG", f"no observed operator other than the sponsor (gated {SH.gated_score(sm):.2f})"
    heavy = [p for p in sm.people if len(p.roles) > SH.MAX_ROLES]
    if heavy:
        return "FLAG", f"{heavy[0].name} holds {len(heavy[0].roles)} of 5 roles"
    if m.get("no_deputy"):
        return "WARN", f"{m['no_deputy']} holdings with no deputy"
    return "PASS", f"operator {ops[0].name} observed; gated {SH.gated_score(sm):.2f}"


def r03(m, gated=True):
    if m["phase"] not in HANDED + ("managed service",):
        return "N/A", "not handed over"
    man = dict(id=m["id"], playbook=None, deviations=[dict(what="playbook", reason="catalog run", owner="FDE",
               review_by=99)], adapter="fieldkit.gateway", eval_suite=True, gold_owner="customer",
               phase="handed over", alert_routes=m["alert_routes"], customer_domain=m["domain"],
               secrets_owner="customer")
    bad = [f for f in lint_engagement(man, Registry(), month=1) if f[0] == "E5"]
    fwd = {r: t for r, t in m.get("forwards", {}).items() if not t.endswith(m["domain"])}
    if not bad and not fwd:
        return "PASS", f"{len(m['alert_routes'])} alert routes, all customer-owned"
    if m.get("alert_deviation"):
        return "DEV", m["alert_deviation"]
    if fwd:
        r, t = next(iter(fwd.items()))
        return "FLAG", f"{r} looks customer-owned but forwards to {t}"
    vendor = [r for r in m["alert_routes"] if not r.endswith(m["domain"])]
    return "FLAG", f"{len(vendor)} alert route(s) to a vendor address: {vendor[0]}"


def r04(m, gated=True):
    c = m.get("commitments", [])
    if not c:
        return "N/A", "no signed commitments"
    need = ("measurer", "documents", "computation", "interval")
    bad = [(x["id"], [k for k in need if not x.get(k)]) for x in c if not all(x.get(k) for k in need)]
    if bad:
        cid, miss = bad[0]
        return "FLAG", f"{cid} lacks {', '.join(miss)}"
    return "PASS", f"{len(c)} commitment(s), each name a measurer, documents, computation and interval"


def r05(m, gated=True):
    steps = m.get("steps", [])
    bad = [(s, c, sorted(set(o) & GUARDED)) for s, c, o in steps if c in MODEL_CLASSES and set(o) & GUARDED]
    if bad:
        s, c, ops = bad[0]
        return "FLAG", f"{s} is a {c} step that performs {', '.join(ops)}"
    model = sum(1 for _, c, _ in steps if c in MODEL_CLASSES)
    return "PASS", f"{len(steps)} steps, {model} model steps, none performs a guarded operation"


def r06(m, gated=True):
    for c in m.get("claims", []):
        h = c["history"]
        for (d0, s0, _), (d1, s1, ev) in zip(h, h[1:]):
            if RANK[s1] > RANK[s0] and not ev:
                return "FLAG", f"{c['id']} rose {s0}->{s1} between day {d0} and day {d1} with no evidence event"
    n = len(m.get("claims", []))
    return ("PASS", f"{n} tracked claim(s), every rise has an evidence event") if n else ("N/A", "no claims")


def r07(m, gated=True):
    g = m.get("gate")
    if not g:
        return "N/A", "no gate read yet"
    k = sum(a for a, _ in g["slices"].values())
    n = sum(b for _, b in g["slices"].values())
    below = [(s, a, b) for s, (a, b) in g["slices"].items() if wilson(a, b)[1] < g["bar"]]
    if g["judged_on"] == "aggregate" and below and k / n >= g["bar"]:
        s, a, b = below[0]
        lo, hi = wilson(a, b)
        return "FLAG", (f"{g['gate']} passed on aggregate {k/n:.1%} ({k:,}/{n:,}); {s} {a/b:.1%} "
                        f"({lo:.1%} to {hi:.1%}) is below {g['bar']:.0%}")
    if g["judged_on"] == "aggregate":
        return "PASS", f"{g['gate']} on aggregate; no slice's interval lies wholly below {g['bar']:.0%}"
    return "PASS", f"{g['gate']} judged per slice; {len(below)} slice(s) below the bar handled by name"


def r08(m, gated=True):
    ev = m.get("accuracy", [])
    if not ev:
        return "N/A", "no accuracy figure in use"
    bad = [e for e in ev if e["scorer"] != "customer" or e["documents"] != "customer"]
    if bad:
        return "FLAG", f"{bad[0]['value']} scored by {bad[0]['scorer']} on {bad[0]['documents']} documents"
    return "PASS", f"{ev[0]['value']} scored by the customer's expert on the customer's documents"


def r09(m, gated=True):
    a = m.get("adapter")
    if a is None:
        return "N/A", "no gateway"
    return ("PASS", "key reread on 401 and on rotation") if a["key_reread"] else ("FLAG", "key read once at start-up")


def r10(m, gated=True):
    t = m.get("thresholds", [])
    bad = [x for x in t if not x.get("chosen_by")]
    if bad:
        return "FLAG", f"threshold {bad[0]['name']}={bad[0]['value']} has no named chooser"
    return ("PASS", f"{len(t)} threshold(s), each with a named chooser") if t else ("N/A", "no thresholds")


def r11(m, gated=True):
    mv = m.get("models", [])
    bad = [x for x in mv if x["version"] in ("latest", "", None)]
    if bad:
        return "FLAG", f"{bad[0]['name']} requests '{bad[0]['version']}'"
    return ("PASS", f"{len(mv)} model(s) pinned") if mv else ("N/A", "no model calls")


def r12(m, gated=True):
    f = m.get("flows")
    if f is None:
        return "N/A", "no data map yet"
    unknown = [x for x in f if not x["retention_known"]]
    if not m.get("map_generated"):
        return "FLAG", f"data map drawn by hand ({len(f)} flows), not generated"
    if unknown:
        return "FLAG", f"{len(unknown)} flow(s) with unknown retention: {unknown[0]['flow']}"
    return "PASS", f"{len(f)} flows generated from the running system, retention known for all"


def r13(m, gated=True):
    rb = m.get("runbooks")
    if rb is None or not _reached(m, "live"):
        return "N/A", "no runbooks yet"
    bad = sum(x["vendor_steps"] for x in rb)
    if bad:
        return "FLAG", f"{bad} step(s) in {sum(1 for x in rb if x['vendor_steps'])} runbook(s) need a vendor login"
    return "PASS", f"{len(rb)} runbooks executable by the customer; last drill {m.get('drill', 'not run')}"


def r14(m, gated=True):
    p = m.get("packs")
    if p is None:
        return "N/A", "no production decisions yet"
    if not p["pinned"] or p["ok"] < p["n"]:
        return "FLAG", f"{p['ok']} of {p['n']} decision packs reconstructable"
    return "PASS", f"{p['ok']} of {p['n']} sampled packs rebuilt from pinned content"


def r15(m, gated=True):
    steps = m.get("playbook_steps")
    if steps is None:
        return "N/A", "no playbook adopted"
    est = set(m.get("estate", ()))
    bad = [(s, sorted(set(n) - est)) for s, n in steps if set(n) - est]
    if bad:
        return "FLAG", f"{bad[0][0]} needs {', '.join(bad[0][1])}, not in the estate"
    return "PASS", f"{len(steps)} playbook steps, every estate need confirmed"


RULES = [r01, r02, r03, r04, r05, r06, r07, r08, r09, r10, r11, r12, r13, r14, r15]


def lint(m, gated=True):
    """Run all fifteen rules. A manifest may carry `why`, the evidence sentence printed for a PASS."""
    out = []
    for i, rule in enumerate(RULES, 1):
        rid = f"R{i:02d}"
        status, detail = rule(m, gated)
        if status == "PASS" and rid in m.get("why", {}):
            detail = m["why"][rid]
        out.append((rid, status, detail))
    return out


def counts(results):
    c = {k: 0 for k in ("PASS", "WARN", "DEV", "FLAG", "N/A")}
    for _, s, _ in results:
        c[s] += 1
    return c
