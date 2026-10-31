"""Data-readiness register: what a document set or table can and cannot support, scored before any model runs.

Deterministic first, model last: these checks are plain code and run on every delivery of data.
"""
from dataclasses import dataclass, field


@dataclass
class ReadinessResult:
    dataset: str
    rows: int
    score: float                       # 0..1, share of checks passed, weighted
    passed: list = field(default_factory=list)
    failed: list = field(default_factory=list)
    blocking: list = field(default_factory=list)

    def ready(self) -> bool:
        return not self.blocking

    def summary(self) -> str:
        head = f"READINESS  {self.dataset}  rows={self.rows}  score={self.score:.2f}  " + \
               ("READY" if self.ready() else "NOT READY")
        body = [f"  FAIL {f}" for f in self.failed] + [f"  pass {p}" for p in self.passed]
        return "\n".join([head] + body)


class ReadinessRegister:
    """Each dataset is registered with its key columns, required columns and value checks."""

    def __init__(self):
        self.specs = {}

    def register(self, name, key, required, checks=None, min_rows=1):
        self.specs[name] = dict(key=key, required=list(required), checks=checks or {}, min_rows=min_rows)

    def assess(self, name, rows):
        spec = self.specs[name]
        res = ReadinessResult(dataset=name, rows=len(rows), score=0.0)
        cols = set(rows[0].keys()) if rows else set()
        weight = total = 0.0

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

        record(f"row count >= {spec['min_rows']}", len(rows) >= spec["min_rows"], 1, True)
        record(f"key column '{spec['key']}' present", spec["key"] in cols, 3, True)
        if spec["key"] in cols:
            keys = [r[spec["key"]] for r in rows]
            record(f"key '{spec['key']}' unique", len(keys) == len(set(keys)), 2, True)
        for c in spec["required"]:
            present = c in cols
            filled = sum(1 for r in rows if r.get(c) not in (None, "")) / max(1, len(rows)) if present else 0
            record(f"'{c}' present and >= 98% filled ({filled:.1%})", present and filled >= 0.98, 1)
        for label, fn in spec["checks"].items():
            share = sum(1 for r in rows if fn(r)) / max(1, len(rows))
            record(f"{label} ({share:.1%})", share >= 0.95, 1)
        res.score = weight / total if total else 0.0
        return res
