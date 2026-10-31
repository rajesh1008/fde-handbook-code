"""Data protection as data (Chapter 35, fieldkit v4.3).

A data map drawn on a whiteboard records what the team believes the system does. This module generates the map from
the deployed configuration instead: one hop per component and one per store, with the data classes that reach it,
who holds it, where it sits, how long it stays, and the clause, BAA or DPA that covers it. Rules for HIPAA, GDPR and
state privacy law run over the hops as lint. A PII scan, patterns first and known values second, checks the stores
the map says hold no personal data. An erasure trace answers "where does this person live, and can we remove them".
Which law applies, and whether a finding is acceptable, is the customer's decision; the module records who made it.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass, field

from .deid import known_value_scan

PERSONAL = {"PHI", "PI", "CLAIM-PI", "EU-PI"}


@dataclass
class Hop:
    name: str
    holder: str
    data: tuple
    location: str
    retention_days: float | None
    basis: str = ""
    kind: str = "process"          # process | store | log | trace | cache | index | backup | weights | access
    deletable: bool = True         # can one subject's records be removed by key
    region_ok: bool = True         # inside the area the data is allowed to sit in
    transfer: str = ""             # transfer mechanism when region_ok is False
    source: str = "generated"      # drawn | generated
    signed: str = ""               # owner sign-off for a store that holds personal data in a log, trace or cache

    @property
    def personal(self):
        return bool(PERSONAL & set(self.data))


@dataclass
class Finding:
    rule: str
    hop: str
    text: str

    def __str__(self):
        return f"  {self.rule:<4} {self.hop:<28} {self.text}"


def generate(config):
    """Walk deployed configuration (components, their inputs, their stores) and emit one hop per thing that touches data."""
    hops = []
    for c in config["components"]:
        data = tuple(c["data"])
        hops.append(Hop(c["name"], c["holder"], data, c["location"], 0 if c.get("stateless", True) else c.get("retention_days"),
                        c.get("basis", ""), "process", True, c.get("region_ok", True), c.get("transfer", "")))
        for s in c.get("stores", []):
            sdata = data if s.get("body", True) else ("META",)
            hops.append(Hop(s["name"], s.get("holder", c["holder"]), sdata, s.get("location", c["location"]),
                            s.get("retention_days"), s.get("basis", c.get("basis", "") if s.get("holder", c["holder"]) == c["holder"] else ""),
                            s.get("kind", "store"), s.get("deletable", True), s.get("region_ok", c.get("region_ok", True)),
                            s.get("transfer", ""), "generated", s.get("signed", "")))
    return hops


def lint(hops, regimes, owner, erasure_window=30):
    """Run the rules for each regime over the hops. owner is the customer (covered entity, controller, insurer)."""
    out = []
    for h in hops:
        if not h.personal:
            continue
        if h.retention_days is None:
            out.append(Finding("R1", h.name, "retention unknown"))
        if "HIPAA" in regimes and "PHI" in h.data:
            if h.holder != owner and not h.basis:
                out.append(Finding("H1", h.name, f"PHI held by {h.holder} with no BAA or clause"))
            if h.kind in ("log", "trace", "cache") and not h.signed:
                out.append(Finding("H2", h.name, f"PHI in a {h.kind} without owner sign-off"))
        if "GDPR" in regimes and "EU-PI" in h.data:
            if not h.region_ok and not h.transfer:
                out.append(Finding("G1", h.name, "outside the EEA with no transfer mechanism"))
            if h.holder != owner and not h.basis:
                out.append(Finding("G2", h.name, f"processed by {h.holder} with no DPA clause"))
            if not h.deletable and (h.retention_days is None or h.retention_days > erasure_window):
                out.append(Finding("G3", h.name, f"cannot erase one subject within {erasure_window} days"))
        if "STATE" in regimes and h.data and "CLAIM-PI" in h.data and h.holder != owner and not h.basis:
            out.append(Finding("S1", h.name, f"claim data held by {h.holder} with no contract clause"))
    return out


def diff(drawn, generated):
    names = {h.name for h in drawn}
    return [h for h in generated if h.name not in names]


def digest(hops):
    """A short fingerprint of the map, so the approver signs this map and can regenerate it to check."""
    blob = json.dumps([asdict(h) | {"source": ""} for h in sorted(hops, key=lambda x: x.name)], sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:12]


def render(hops, findings=()):
    flagged = Counter(f.hop for f in findings)
    rows = []
    for h in hops:
        ret = "unknown" if h.retention_days is None else ("none" if h.retention_days == 0 else f"{h.retention_days:g}d")
        rows.append(f"  {h.name:<28} {h.holder:<12} {'/'.join(h.data):<9} {ret:>8}  {h.basis or '-':<16} "
                    f"{'FLAG ' + str(flagged[h.name]) if flagged[h.name] else 'ok'}")
    return "\n".join(rows)


# ----- PII scan ------------------------------------------------------------------------------------------------
SCAN_PATTERNS = [
    ("MRN", r"\bMRN[:# ]*\d{7}\b"),
    ("DOB", r"\b(?:DOB|born)[: ]+\d{1,2}/\d{1,2}/\d{4}\b"),
    ("PHONE", r"\b\d{3}[ .-]\d{3}[ .-]\d{4}\b"),
    ("SSN", r"\b\d{3}-\d{2}-\d{4}\b"),
    ("EMAIL", r"\b[\w.]+@[\w-]+\.[\w.]+\b"),
]


def mask(value):
    return value[:1] + "***" + hashlib.sha256(value.encode()).hexdigest()[:4]


@dataclass
class ScanReport:
    entries: int = 0
    hit_entries: int = 0
    by_class: Counter = field(default_factory=Counter)
    pattern_only: int = 0
    examples: list = field(default_factory=list)

    @property
    def clean(self):
        return self.hit_entries == 0

    def summary(self):
        cls = ", ".join(f"{k} {v}" for k, v in sorted(self.by_class.items())) or "none"
        return (f"  entries scanned {self.entries}   entries with personal data {self.hit_entries}   "
                f"found by patterns alone {self.pattern_only}\n  by class: {cls}")


def pii_scan(entries, known=None):
    """Scan log entries. Patterns catch formatted identifiers; the known-value list (the customer's own roster of
    subjects in the period) catches names in free text, which patterns miss. Values are never printed, only masked."""
    rep = ScanReport()
    for e in entries:
        rep.entries += 1
        hits = []
        for cls, pat in SCAN_PATTERNS:
            hits += [(cls, m.group(0)) for m in re.finditer(pat, e)]
        pat_hit = bool(hits)
        for values in known or []:
            hits += [("NAME" if lab.upper().endswith("NAME") else lab.upper(), v)
                     for lab, v in known_value_scan(e, values)]
        if hits:
            rep.hit_entries += 1
            rep.pattern_only += pat_hit
            for cls in {c for c, _v in hits}:
                rep.by_class[cls] += 1      # entries carrying the class, not raw matches
            if len(rep.examples) < 3:
                rep.examples.append(", ".join(f"{c}={mask(v)}" for c, v in sorted(set(hits))[:3]))
    return rep


# ----- erasure and minimum necessary ---------------------------------------------------------------------------
def erasure_trace(hops, window=30):
    """For one subject: where their data can sit and how it leaves each place."""
    out = []
    for h in hops:
        if not h.personal or h.retention_days == 0:
            continue
        if h.deletable:
            how, days = "delete by key", 1
        elif h.retention_days is not None and h.retention_days <= window:
            how, days = "expires", h.retention_days
        else:
            how, days = "cannot erase", h.retention_days
        out.append((h.name, how, days, how != "cannot erase"))
    return out


def minimum_necessary(read, needed):
    extra = sorted(set(read) - set(needed))
    return extra, (len(extra) / len(set(read)) if read else 0.0)
