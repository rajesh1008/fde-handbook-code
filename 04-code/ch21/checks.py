"""Pennant's quality checks at the door (Chapter 21 lab)."""
import _paths  # noqa: F401
from fieldkit.quality import Check, QualityScorer
from pennant import REQUIRED, LEGIBLE_AT, container_ok

FIELDS = sorted({f for req in REQUIRED.values() for f in req})
MEANINGS = {
    "currency": "the ISO currency code of the invoice total (the country does not tell us)",
    "total": "the invoice total as printed",
    "lines": "the line amounts that make up the total",
    "container": "the 11-character container number (ISO 6346)",
    "gross_kg": "gross weight in kilograms as declared by the shipper",
    "incoterms": "the Incoterms rule for this shipment",
    "packages": "number of packages",
    "hs_codes": "HS commodity codes",
    "declarant_id": "the declarant's EORI number",
    "shipper": "shipper name", "consignee": "consignee name", "carrier": "carrier name",
}


def _has(f):
    def fn(d):
        if f not in REQUIRED[d["kind"]]:
            return "n/a"
        return None if d.get(f) not in (None, "", []) else f"{f} missing"
    return fn


def _legible(d):
    return None if d["legibility"] >= LEGIBLE_AT else f"page confidence {d['legibility']:.2f}"


def _sums(d):
    if "lines" not in REQUIRED[d["kind"]] or not d.get("lines") or d.get("total") is None:
        return "n/a"
    return None if abs(sum(d["lines"]) - d["total"]) < 0.01 else f"lines sum to {sum(d['lines']):,.2f}, total says {d['total']:,.2f}"


def _container(d):
    if "container" not in REQUIRED[d["kind"]] or not d.get("container"):
        return "n/a"
    return None if container_ok(d["container"]) else f"container {d['container']} fails ISO 6346 check digit"


CHECKS = [Check(f"has {f}", "completeness", _has(f)) for f in FIELDS] + [
    Check("legible", "legibility", _legible),
    Check("lines sum to total", "consistency", _sums),
    Check("container check digit", "consistency", _container),
]


def scorer(version="pennant-qs-1.0"):
    return QualityScorer(CHECKS, version)
