"""Pennant's first shadow week, days 124 to 130: 2,100 documents (deterministic stand-in).

Nothing here is Pennant data. Draws are keyed by document or shipment id through
sha256 (pennant.u), so every run produces the same week. The truth fields that
start with an underscore are what Pennant's reconciliation team ruled; the
pipeline never reads them.
"""
import _paths  # noqa: F401
from pennant import u, _iso6346_check, REQUIRED
from fieldkit.lineage import RefTables, digest

DAYS = tuple(range(124, 131))
N_DOCS, N_SHIP = 2100, 780
DAY_SHARE = tuple(zip(DAYS, (0.17, 0.18, 0.17, 0.17, 0.16, 0.08, 0.07)))   # days 129 and 130 are a weekend
CARRIERS = {"HLSU": "Harbor Line Shipping", "BRFU": "Blue Ridge Freight", "DCLU": "Delta Crescent Lines",
            "NWCU": "Northwind Cargo", "LKTU": "Lakeshore Transport", "IRCU": "Iron Range Carriers",
            "GPMU": "Gulfport Marine", "RBLU": "Riverbend Logistics", "SFWU": "Summit Freightways",
            "CPXU": "Cedar Point Express", "ATCU": "Atlas Coastal"}
CURRENCY = {"US": "USD", "MX": "MXN", "CA": "CAD", "DE": "EUR", "NL": "EUR", "BE": "EUR", "FR": "EUR",
            "IT": "EUR", "PL": "PLN", "CN": "CNY", "VN": "VND"}
FX_ROWS = {"USD": 1.0, "EUR": 1.0853, "MXN": 0.0581, "CAD": 0.7342, "PLN": 0.2521, "CNY": 0.1387, "VND": 0.0000394}
RATE_CARD_ACC = {"fuel surcharge", "chassis", "terminal handling"}
PAPER_KINDS = (("bill of lading", 0.30), ("freight invoice", 0.20), ("commercial invoice", 0.20),
               ("packing list", 0.20), ("customs declaration", 0.10))
KEYS = {"bill of lading": ("container", "bol_no"), "freight invoice": ("container", "bol_no"),
        "packing list": ("container", "booking_ref"), "commercial invoice": ("booking_ref", "bol_no"),
        "customs declaration": ("booking_ref", "container")}
CHANNEL = (("edi", 0.40), ("scan", 0.44), ("photo", 0.16))
# defect rates by channel (stand-in values, calibrated to the shape of Chapter 21's sample)
P = {
    "scan":  dict(missing=0.040, inconsistent=0.030, bad_container=0.015, occluded=0.002, misread=0.008,
                  unknown_layout=0.010, low_date=0.060),
    "photo": dict(missing=0.050, inconsistent=0.030, bad_container=0.015, occluded=0.030, misread=0.030,
                  unknown_layout=0.010, low_date=0.140),
    "edi":   dict(envelope=0.012),
}
DISCREPANCY = 0.070        # real business disagreements, any channel
DISC_BY_KIND = {"bill of lading": ("weight", "date", "container"), "packing list": ("weight",),
                "freight invoice": ("amount", "accessorial", "weight"), "commercial invoice": ("value",),
                "customs declaration": ("value",)}
RULE_OF = {"container": "R1", "weight": "R2", "amount": "R3", "accessorial": "R4", "value": "R5", "date": "R6"}


def container(prefix, s):
    body = f"{prefix}{(311000 + s * 37) % 1000000:06d}"
    return body + str(_iso6346_check(body))


def fx_registry():
    refs = RefTables()
    vid = refs.register("fx_rates", FX_ROWS, as_of="day 123 close", owner="Marisol Vega")
    return refs, vid


def bookings():
    """The TMS view of each shipment, as the 02:00 Central export carries it."""
    pre = list(CARRIERS)
    out = {}
    for s in range(N_SHIP):
        pair = u(s // 2, "pair") < 0.30               # consolidations: two containers, same shipper and lane
        base = s - (s % 2) if pair else s
        country = list(CURRENCY)[int(u(base, "country") * 11)]
        gross = round(4000 + 18000 * u(base, "kg"), 0) * (1 + (0.012 if (pair and s % 2) else 0))
        out[s] = dict(shipment=s, booking_ref=f"PN-{48000 + s}", bol_no=f"{pre[int(u(base, 'car') * 11)][:2]}{702000 + s}",
                      container=container(pre[int(u(base, 'car') * 11)], s), carrier=CARRIERS[pre[int(u(base, 'car') * 11)]],
                      country=country, currency=CURRENCY[country], gross_kg=gross,
                      chargeable_kg=round(max(gross, 1.6 * gross * (0.55 + 0.1 * u(base, "vol"))), 0),
                      contract_usd=round(900 + 6200 * u(base, "rate"), 2), declared_value=round(20000 + 180000 * u(base, "val"), 2),
                      delivered_day=118 + int(u(base, "dd") * 12), sibling=(s ^ 1) if pair else None,
                      customs_hold=u(s, "hold") < 0.03, late=u(s, "late") < 0.01)
    return out


def _pick(r, table):
    acc = 0.0
    for k, w in table:
        acc += w
        if r < acc:
            return k
    return table[-1][0]


def feed():
    bk = bookings()
    docs = []
    for i in range(N_DOCS):
        did = f"W{i + 1:05d}"
        ch = _pick(u(did, "channel"), CHANNEL)
        kind = "freight invoice" if ch == "edi" else _pick(u(did, "kind"), PAPER_KINDS)
        s = int(u(did, "ship") * N_SHIP)
        b = bk[s]
        rate = FX_ROWS[b["currency"]]
        d = dict(doc_id=did, day=_pick(u(did, "day"), DAY_SHARE), channel=ch, kind=kind, layout=f"L{1 + int(u(did, 'lay') * 12):02d}",
                 sender=b["carrier"] if kind == "freight invoice" else "Northgate Fabrication Ltd", carrier=b["carrier"],
                 shipper="Northgate Fabrication Ltd", consignee="Pennant consignee", incoterms="FCA", packages=12,
                 hs_codes=["8431.49"], declarant_id="NL812345678", legibility=1.0, _ship=s, _truth=set(),
                 zone_conf={"container": 0.97, "bol_no": 0.97})
        for k in KEYS.get(kind, ()):
            d[k] = b[k]
        if kind == "freight invoice":
            d.update(bol_no=b["bol_no"], booking_ref=b["booking_ref"])
            crate = rate * (1 + (0.008 * u(did, "cfx") - 0.004 if b["currency"] != "USD" else 0))   # the carrier's own rate that day
            base = round(b["contract_usd"] * 0.88 / crate, 2)
            acc = [("fuel surcharge", round(b["contract_usd"] * 0.12 / crate, 2))]
            d.update(currency=b["currency"], gross_kg=b["chargeable_kg"], lines=[base] + [a for _, a in acc],
                     acc=[n for n, _ in acc], total=round(base + acc[0][1], 2))
        elif kind in ("bill of lading", "packing list"):
            d.update(gross_kg=b["gross_kg"])
            if kind == "bill of lading":
                d.update(delivery_day=b["delivered_day"], date_conf=0.97)
        else:
            val = round(b["declared_value"] / rate, 2)
            d.update(currency=b["currency"], total=val, lines=[round(val * 0.6, 2), round(val - round(val * 0.6, 2), 2)])
        if ch == "edi":
            if u(did, "env") < P["edi"]["envelope"]:
                d["_truth"].add("envelope")
        else:
            p = P[ch]
            d["legibility"] = round((0.70 + 0.29 * u(did, "leg")) if ch == "scan" else (0.56 + 0.43 * u(did, "leg")), 2)
            if d["legibility"] < 0.65:
                d["_truth"].add("illegible")
            req = REQUIRED[kind]
            if u(did, "miss") < p["missing"]:
                f = req[int(u(did, "mf") * len(req))]
                d[f] = None
                d["_truth"].add("missing")
            if "lines" in req and d.get("lines") and u(did, "sum") < p["inconsistent"] / 0.5:
                if u(did, "sum2") < 0.5:
                    d["lines"] = [d["lines"][0] + 100.0] + d["lines"][1:]
                    d["_truth"].add("inconsistent")
            if kind in ("bill of lading", "packing list", "freight invoice") and d.get("container"):
                if u(did, "cd") < p["bad_container"]:
                    c = d["container"]
                    d["container"] = c[:10] + str((int(c[10]) + 3) % 10)
                    d["_truth"].add("bad_container")
                elif u(did, "thumb") < p["occluded"]:
                    d["_truth"].add("occluded")
                    d["container"] = d["container"][:6]          # the OCR layer sees only what the thumb leaves
                    d["zone_conf"] = dict(d["zone_conf"], container=round(0.08 + 0.2 * u(did, "zc"), 2))
            if u(did, "mr") < p["misread"]:
                d["_misread"] = True
            if u(did, "unk") < p["unknown_layout"]:
                d["layout"] = "L??"
            if kind == "bill of lading" and u(did, "hd") < p["low_date"]:
                d["date_conf"] = round(0.55 + 0.34 * u(did, "hdc"), 2)
        if not d["_truth"] and u(did, "disc") < DISCREPANCY:
            t = DISC_BY_KIND[kind][int(u(did, "dt") * len(DISC_BY_KIND[kind]))]
            d["_disc"] = t
            if t == "amount":
                if u(did, "amt") < 0.5:      # a flat over-billing, the day-66 kind
                    d["lines"][0] = round(d["lines"][0] + 412.50 / rate, 2)
                else:                         # fuel surcharge billed at 14% instead of the contract's 12%
                    d["lines"][1] = round(d["lines"][1] * 14 / 12, 2)
                d["total"] = round(sum(d["lines"]), 2)
            elif t == "accessorial":
                extra = round(185.00 / rate, 2)
                d["lines"].append(extra); d["acc"].append("detention"); d["total"] = round(sum(d["lines"]), 2)
            elif t == "weight":
                d["gross_kg"] = round(d["gross_kg"] * 1.09, 0)
            elif t == "value":
                d["total"] = round(d["total"] * 1.04, 2); d["lines"] = [round(d["total"] * 0.6, 2), round(d["total"] - round(d["total"] * 0.6, 2), 2)]
            elif t == "date":
                d["delivery_day"] = d["delivery_day"] + 3
            elif t == "container":
                d["container"] = container("TGHU", 900000 + s)   # carrier swapped the box
        d["_sha256"] = digest([did, {k: v for k, v in d.items() if not k.startswith("_")}])
        docs.append(d)
    return docs, bk


def x12_210(docs):
    """One X12 210 interchange per carrier per day; a few sets arrive with a bad SE count."""
    out = {}
    for d in docs:
        if d["channel"] != "edi":
            continue
        key = (d["carrier"], d["day"])
        out.setdefault(key, [])
        n = 7 + (1 if "envelope" in d["_truth"] else 0)
        st = f"{len(out[key]) + 1:04d}"
        segs = [f"ST*210*{st}", f"B3**{d['doc_id']}*{d['bol_no']}*PP**{d['day']}*{d['total']:.2f}",
                f"N9*BM*{d['bol_no']}", f"N9*PO*{d['booking_ref']}", f"N7**{d['container'] or ''}",
                f"L3*{d['gross_kg']:.0f}*G***{d['total']:.2f}*{d['currency']}", f"SE*{n}*{st}"]
        out[key].append("~".join(segs))
    text = {}
    for (car, day), sets in out.items():
        ctl = f"{abs(hash((car, day))) % 10**9:09d}" if False else f"{int(digest([car, day]), 16) % 10**9:09d}"
        text[(car, day)] = f"ISA*00*          *00*          *ZZ*{car[:15]:<15}*ZZ*PENNANT        *{day}*0200*U*00401*{ctl}*0*P*>~" + \
            "~".join(sets) + f"~IEA*{len(sets)}*{ctl}~"
    return text
