"""fieldkit v4.5 (Chapter 37): the gate tracker and the accountable executive's pack.

A gate is passed by evidence, not by a date in a plan. Each gate record carries its entry evidence (what had to be
true before the gate could be held), its exit criteria (bars the customer's owner wrote down), the measurements
offered against them (who measured, on what, of what kind) and the signer. The tracker enforces three rules:

  1. Per-class exit. A criterion with `per` set is judged on every class as well as on the aggregate. A class whose
     interval sits wholly below the bar fails; a class whose interval spans the bar is "not shown". An aggregate
     pass with a failing or unshown class is not a pass, unless a named person takes the class out of scope by a
     condition (excluded) or accepts an unshown class in writing (accepted), each with a day.
  2. Evidence kind. Customer-outcome criteria accept only measurements of kind "customer measurement".
     Model confidence, a fluent summary and a component test are recorded and refused.
  3. Order. A gate cannot be effective while an earlier gate is not passed; a later decision is held, not counted.

`pack()` assembles the eight artifacts an accountable executive needs and reports each as present, partial or
missing; `residual_lint()` refuses a residual risk without a named acceptor, a day and a review day.
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field

from fieldkit.security import is_person

GATES = ("Architecture Review", "Build Complete", "Shadow Exit", "Model-Risk Approval", "Live Stable")
PACK = ("decision record", "lineage", "model and prompt versions", "evaluation at the time", "human review",
        "authority boundary", "incident history", "monitoring")
KINDS = ("customer measurement", "component test", "model confidence", "fluent response", "log")


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson interval for k successes in n trials."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


@dataclass
class Criterion:
    key: str
    text: str
    bar: float                    # proportion, e.g. 0.80
    higher_is_better: bool = True
    per: str | None = None        # name of the class dimension judged separately, e.g. "document class"
    outcome: bool = True          # a customer-outcome criterion (only customer measurements count)
    owner: str = ""               # who wrote the bar


@dataclass
class Measurement:
    key: str
    k: int
    n: int
    scope: str = "all"            # "all" or a class name
    kind: str = "customer measurement"
    measured_by: str = ""
    on: str = ""
    day: int | None = None

    def __post_init__(self):
        assert self.kind in KINDS, self.kind

    @property
    def rate(self) -> float:
        return self.k / self.n if self.n else 0.0


@dataclass
class Line:
    key: str
    scope: str
    verdict: str                  # met, below, not shown, refused, missing
    detail: str


def judge(c: Criterion, m: Measurement) -> Line:
    lo, hi = wilson(m.k, m.n)
    shown = f"{m.rate:.1%} ({m.k:,}/{m.n:,}; {lo:.1%} to {hi:.1%})"
    if c.outcome and m.kind != "customer measurement":
        return Line(c.key, m.scope, "refused", f"{m.kind} cannot show a customer outcome")
    if c.higher_is_better:
        bad = hi < c.bar
        if m.rate >= c.bar:
            return Line(c.key, m.scope, "met", shown)
    else:
        if m.rate <= c.bar:
            return Line(c.key, m.scope, "met", shown)
        bad = lo > c.bar
    return Line(c.key, m.scope, "below" if bad else "not shown", shown)


@dataclass
class GateRecord:
    gate: str
    entry: list = field(default_factory=list)        # (text, reference) pairs
    criteria: list = field(default_factory=list)
    measurements: list = field(default_factory=list)
    signer: str = ""
    decided: int | None = None
    conditions: list = field(default_factory=list)   # (text, owner, due_day)
    accepted: list = field(default_factory=list)     # (key, scope, person, day): a "not shown" class accepted in writing
    excluded: list = field(default_factory=list)     # (key, scope, person, day): a class taken out of scope by a condition

    def __post_init__(self):
        assert self.gate in GATES, self.gate

    def _waived(self, line: Line) -> Line:
        for key, scope, person, day in self.excluded:
            if (key, scope) == (line.key, line.scope) and is_person(person) and day is not None:
                return Line(line.key, line.scope, "excluded", f"{line.detail}; out of scope by {person}, day {day}")
        if line.verdict == "not shown":
            for key, scope, person, day in self.accepted:
                if (key, scope) == (line.key, line.scope) and is_person(person) and day is not None:
                    return Line(line.key, line.scope, "accepted", f"{line.detail}; accepted by {person}, day {day}")
        return line

    def evaluate(self, per_class: bool = True) -> list[Line]:
        out = []
        for c in self.criteria:
            ms = [m for m in self.measurements if m.key == c.key]
            agg = [m for m in ms if m.scope == "all"]
            if not agg:
                out.append(Line(c.key, "all", "missing", "no measurement offered"))
            for m in agg:
                out.append(judge(c, m))
            if c.per and per_class:
                for m in ms:
                    if m.scope != "all":
                        out.append(self._waived(judge(c, m)))
        return out

    def status(self, per_class: bool = True) -> str:
        lines = self.evaluate(per_class)
        cond_ok = all(is_person(o) and d is not None for _, o, d in self.conditions)
        if not self.entry:
            return "not held: no entry evidence"
        if any(l.verdict not in ("met", "accepted", "excluded") for l in lines):
            return "blocked"
        if not is_person(self.signer) or self.decided is None:
            return "awaiting signature"
        if not cond_ok:
            return "blocked: condition without a person and a day"
        return "passed with conditions" if self.conditions else "passed"


class Tracker:
    """Five gate records for one customer, held in order."""

    def __init__(self, customer: str):
        self.customer = customer
        self.records: dict[str, GateRecord] = {}

    def add(self, rec: GateRecord):
        self.records[rec.gate] = rec
        return rec

    def effective(self, per_class: bool = True) -> list[tuple[str, str, int | None, str]]:
        """(gate, status, day effective, note) in gate order; a later pass is held until every earlier gate passes."""
        rows, open_before, last_day = [], None, 0
        for g in GATES:
            r = self.records.get(g)
            if r is None:
                rows.append((g, "not started", None, ""))
                open_before = open_before or g
                continue
            st = r.status(per_class)
            passed = st.startswith("passed")
            if passed and open_before:
                rows.append((g, "held", None, f"decided day {r.decided}; waits on {open_before}"))
                continue
            if passed:
                day = max(r.decided or 0, last_day)
                note = "" if day == r.decided else f"decided day {r.decided}; effective with the earlier gate"
                rows.append((g, st, day, note))
                last_day = day
            else:
                rows.append((g, st, None, ""))
                open_before = open_before or g
        return rows

    def held_back(self, per_class: bool = True) -> list[str]:
        return [g for g, st, _, _ in self.effective(per_class) if st == "held"]


@dataclass
class Artifact:
    name: str
    ref: str = ""
    owner: str = ""
    day: int | None = None
    status: str = "missing"   # present, partial, missing
    gap: str = ""

    def __post_init__(self):
        assert self.name in PACK and self.status in ("present", "partial", "missing"), (self.name, self.status)


def pack(artifacts) -> dict:
    """Eight artifacts in fixed order, with a digest over what is present so the executive can cite one value."""
    by = {a.name: a for a in artifacts}
    rows = [by.get(n, Artifact(n)) for n in PACK]
    for a in rows:
        if a.status == "present" and (not a.ref or a.day is None or not is_person(a.owner)):
            a.status, a.gap = "partial", a.gap or "present but without a reference, an owner and a day"
    h = hashlib.sha256("|".join(f"{a.name}:{a.ref}:{a.owner}:{a.day}:{a.status}" for a in rows).encode())
    counts = {s: sum(a.status == s for a in rows) for s in ("present", "partial", "missing")}
    return dict(rows=rows, counts=counts, digest=h.hexdigest()[:12], complete=counts["present"] == len(PACK))


@dataclass
class ResidualRisk:
    text: str
    accepted_by: str = ""
    day: int | None = None
    review_day: int | None = None
    control: str = ""


def residual_lint(risks) -> list[str]:
    out = []
    for r in risks:
        if not is_person(r.accepted_by):
            out.append(f"'{r.text}': no named person accepted it")
        if r.day is None or r.review_day is None:
            out.append(f"'{r.text}': needs the day accepted and a review day")
        if not r.control:
            out.append(f"'{r.text}': no control named while it is carried")
    return out
