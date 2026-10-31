"""Pennant Logistics document feed: a deterministic stand-in (Chapter 21 lab).

Not Pennant's data. A seeded generator that reproduces the shape the team saw on the
day-64 sample: 41 layouts in five document kinds from eleven countries, a long tail of
low-volume layouts, mailbox scans and phone photos next to clean EDI, and five
kinds of defect (illegible page, missing field, lines that do not sum, a container
number whose ISO 6346 check digit is wrong, and a legible page the OCR misread, which no door check can see). Every random draw is keyed by document id,
so a run is reproducible and the with/without comparisons are paired.
"""
import hashlib

N_DOCS = 2000
COUNTRIES = {  # code: (currency, decimal separator, date order)
    "US": ("USD", ".", "mdy"), "MX": ("MXN", ".", "dmy"), "CA": ("CAD", ".", "ymd"),
    "DE": ("EUR", ",", "dmy"), "NL": ("EUR", ",", "dmy"), "BE": ("EUR", ",", "dmy"),
    "FR": ("EUR", ",", "dmy"), "IT": ("EUR", ",", "dmy"), "PL": ("PLN", ",", "dmy"),
    "CN": ("CNY", ".", "ymd"), "VN": ("VND", ".", "dmy"),
}
KINDS = ("bill of lading", "commercial invoice", "packing list", "customs declaration", "freight invoice")
REQUIRED = {
    "bill of lading": ("container", "shipper", "consignee", "gross_kg"),
    "commercial invoice": ("currency", "total", "lines", "incoterms"),
    "packing list": ("container", "gross_kg", "packages"),
    "customs declaration": ("hs_codes", "currency", "total", "declarant_id"),
    "freight invoice": ("currency", "total", "lines", "container", "carrier"),
}
BASE_EXCEPTION = 0.10      # real business disagreements on a clean document
DEFECT_EXCEPTION = {"illegible": 0.80, "missing": 0.65, "inconsistent": 0.90, "bad_container": 0.85, "misread": 0.70}
MARGINAL_EXCEPTION = 0.12   # legible enough to pass, poor enough to hurt (0.65 to 0.75)
LEGIBLE_AT = 0.65
MISS_P, SUM_P, CD_P, MISREAD_P = 0.05, 0.04, 0.025, 0.012


def u(*key) -> float:
    h = hashlib.sha256("|".join(map(str, key)).encode()).hexdigest()
    return int(h[:13], 16) / 16 ** 13


def _iso6346_check(code10: str) -> int:
    vals, v = {}, 10
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if v % 11 == 0:
            v += 1
        vals[ch] = v
        v += 1
    total = sum((vals[c] if c.isalpha() else int(c)) * 2 ** i for i, c in enumerate(code10))
    return total % 11 % 10


def container_ok(c: str) -> bool:
    return len(c) == 11 and c[:4].isalpha() and c[4:].isdigit() and _iso6346_check(c[:10]) == int(c[10])


def layouts():
    names = list(COUNTRIES)
    out = []
    for i in range(41):
        kind = KINDS[i % 5]
        country = names[(i * 7 + i // 5) % 11]
        if kind == "freight invoice" and country in ("US", "CA", "MX"):
            channel = "edi"
        elif i % 6 == 5 or i >= 30 and i % 2 == 0:
            channel = "photo"
        else:
            channel = "scan"
        out.append(dict(layout=f"L{i + 1:02d}", kind=kind, country=country, channel=channel))
    return out


def volumes(n=N_DOCS, top=12, target=0.76):
    lo, hi = 0.0, 3.0
    for _ in range(60):
        s = (lo + hi) / 2
        w = [(i + 1) ** -s for i in range(41)]
        share = sum(w[:top]) / sum(w)
        lo, hi = (s, hi) if share < target else (lo, s)
    raw = [x / sum(w) * n for x in w]
    counts = [int(x) for x in raw]
    for i in sorted(range(41), key=lambda i: raw[i] - counts[i], reverse=True)[: n - sum(counts)]:
        counts[i] += 1
    return counts


def fmt_amount(x: float, sep: str) -> str:
    s = f"{x:,.2f}"
    return s if sep == "." else s.replace(",", "_").replace(".", ",").replace("_", ".")


def feed(n=N_DOCS):
    docs, k = [], 0
    for lay, cnt in zip(layouts(), volumes(n)):
        cur, sep, dorder = COUNTRIES[lay["country"]]
        for j in range(cnt):
            k += 1
            did = f"P{k:05d}"
            r = lambda tag: u(did, tag)
            lines = [round(200 + 4000 * r(f"line{i}"), 2) for i in range(1 + int(r("nlines") * 5))]
            invoice_cur = "USD" if lay["country"] != "US" and r("usd") < 0.30 else cur
            owner = ["HLSU", "BRFU", "MSKU", "TGHU", "CMAU"][int(r("own") * 5)]
            body = f"{owner}{int(r('ser') * 1e6):06d}"
            cont = body + str(_iso6346_check(body))
            leg = 1.0 if lay["channel"] == "edi" else (
                0.71 + 0.28 * r("leg") if lay["channel"] == "scan" else 0.45 + 0.53 * r("leg"))
            d = dict(doc_id=did, layout=lay["layout"], kind=lay["kind"], country=lay["country"],
                     channel=lay["channel"], legibility=round(leg, 3), currency=invoice_cur,
                     lines=lines, total=round(sum(lines), 2), amount_text=fmt_amount(round(sum(lines), 2), sep),
                     container=cont, shipper="Northgate Fabrication Ltd", consignee="Pennant Logistics",
                     gross_kg=round(800 + 18000 * r("kg"), 1), packages=1 + int(r("pk") * 40),
                     incoterms="FOB", hs_codes=["8471.30"], declarant_id="NL123456789",
                     carrier=["Harbor Line Shipping", "Blue Ridge Freight"][int(r("car") * 2)],
                     day=1 + int(r("day") * 28), month=1 + int(r("mon") * 12), date_order=dorder,
                     _truth=set(), _true_currency=invoice_cur, _printed=round(sum(lines), 2))
            req = REQUIRED[lay["kind"]]
            if r("miss") < MISS_P:
                f = req[int(r("missf") * len(req))]
                d[f] = None
                d["_truth"].add("missing")
            if "lines" in req and r("sum") < SUM_P:
                d["total"] = round(d["total"] + 100 * (1 + int(r("sumd") * 9)), 2)
                d["_truth"].add("inconsistent")
            if "container" in req and d["container"] and r("cd") < CD_P:
                d["container"] = d["container"][:10] + str((int(d["container"][10]) + 3) % 10)
                d["_truth"].add("bad_container")
            if r("misread") < MISREAD_P:     # a legible page the OCR read wrong: invisible at the door
                d["_truth"].add("misread")
            if leg < LEGIBLE_AT:
                d["_truth"].add("illegible")
            docs.append(d)
    return docs


def exception_prob(d) -> float:
    p = BASE_EXCEPTION
    for t in d["_truth"]:
        p = max(p, DEFECT_EXCEPTION[t])
    if not d["_truth"] and LEGIBLE_AT <= d["legibility"] < 0.75:
        p = MARGINAL_EXCEPTION
    return p


def is_exception(d, attempt="first") -> bool:
    """Downstream reconciliation raises an exception (paired draw per document)."""
    return u(d["doc_id"], "exc", attempt) < exception_prob(d)
