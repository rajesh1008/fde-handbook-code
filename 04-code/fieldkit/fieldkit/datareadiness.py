"""Data-readiness register, field level (fieldkit v2, Chapter 15).

Version 1 (Chapter 3) checks a delivery: row count, key, required columns, value checks. Version 2
registers every field before the data arrives, with four facts the customer's people own:

    meaning       what the field says, in the words of the customer's expert who uses it
    entitlement   who may read it, and whether it may be delivered at all
    freshness     how old a delivery may be before a result built on it is stale
    owner         the customer-side person who answers questions about the field

and the work each field supports, so a missing column is reported as the work it stops.
Deterministic first, model last: nothing here calls a model.
"""
from dataclasses import dataclass, field
from typing import Optional

from .readiness import ReadinessRegister, ReadinessResult


@dataclass
class FieldSpec:
    name: str
    meaning: str
    owner: str
    entitlement: str = "named readers"
    deliver: bool = True                 # False: the field must not appear in any delivery
    freshness_days: Optional[int] = None  # None: freshness judged on the delivery, not the field
    supports: tuple = ()


@dataclass
class FieldReadiness(ReadinessResult):
    fields: list = field(default_factory=list)       # report lines
    lost: list = field(default_factory=list)         # work a missing field stops
    unregistered: list = field(default_factory=list)

    def summary(self) -> str:
        out = [super().summary()]
        out.append(f"FIELDS  delivered={self.delivered}  registered={self.registered}  "
                   f"unregistered={len(self.unregistered)}")
        out += ["  " + line for line in self.fields]
        if self.lost:
            out.append("CANNOT YET: " + "; ".join(self.lost))
        return "\n".join(out)


class DataReadinessRegister(ReadinessRegister):
    def __init__(self):
        super().__init__()
        self.fields = {}
        self.freshness = {}

    def register_fields(self, name, fields, max_age_days=None):
        self.fields[name] = {f.name: f for f in fields}
        self.freshness[name] = max_age_days

    def card(self, name) -> str:
        """The register entry as the customer's people review it, before any data arrives."""
        lines = [f"REGISTER  {name}  (max delivery age {self.freshness.get(name)} days)",
                 f"{'field':<16}{'owner':<17}{'entitlement':<31}meaning"]
        for f in self.fields[name].values():
            ent = f.entitlement + ("" if f.deliver else " (do not deliver)")
            lines.append(f"{f.name:<16}{f.owner:<17}{ent:<31}{f.meaning}")
        return "\n".join(lines)

    def assess(self, name, rows, extracted_day=None, delivered_day=None):
        base = super().assess(name, rows)
        res = FieldReadiness(**{k: getattr(base, k) for k in
                                ("dataset", "rows", "score", "passed", "failed", "blocking")})
        specs = self.fields.get(name, {})
        cols = list(rows[0].keys()) if rows else []
        res.delivered, res.registered = len(cols), len(specs)
        res.unregistered = [c for c in cols if c not in specs]
        total = self._total(name, cols)
        weight = base.score * total

        def record(label, ok, w=1.0, block=False):
            nonlocal weight, total
            total += w
            if ok:
                weight += w
                res.passed.append(label)
            else:
                res.failed.append(label)
                if block:
                    res.blocking.append(label)

        breaches = [c for c in cols if c in specs and not specs[c].deliver]
        record("no do-not-deliver field present" + (f" (found: {', '.join(breaches)})" if breaches else ""),
               not breaches, 3, True)
        record("every delivered field registered" +
               (f" (unregistered: {', '.join(res.unregistered)})" if res.unregistered else ""),
               not res.unregistered, 1)
        undocumented = [f.name for f in specs.values() if not (f.meaning and f.owner)]
        record("every registered field has a meaning and an owner", not undocumented, 1)
        limit = self.freshness.get(name)
        if limit is not None and extracted_day is not None and delivered_day is not None:
            age = delivered_day - extracted_day
            record(f"delivery age {age} days <= {limit}", age <= limit, 1)
        res.score = weight / total if total else 0.0

        for f in specs.values():
            if not f.deliver:
                state = "withheld, as registered" if f.name not in cols else "DELIVERED, must not be"
            else:
                state = "present" if f.name in cols else "MISSING"
            res.fields.append(f"{f.name:<16}{state:<24}owner {f.owner}")
            if f.deliver and f.name not in cols:
                res.lost += [f"{s} (needs {f.name})" for s in f.supports]
        for c in res.unregistered:
            res.fields.append(f"{c:<16}{'UNREGISTERED':<24}owner unknown")
        return res

    def _total(self, name, cols):
        spec = self.specs[name]
        return 1 + 3 + (2 if spec["key"] in cols else 0) + len(spec["required"]) + len(spec["checks"])
