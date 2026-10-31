"""fieldkit.cadence (book layer v1.6, Chapter 13): the two-week cadence as data.

What it holds:
  Item        a backlog item with priority P0-P3, an accountable owner, acceptance criteria and evidence
  plan_sprint the ordering rule with a displacement guard: P3 enters only when it displaces nothing in P0-P2
  Record      a decision record (owner, due day, options, decision, evidence, milestone impact)
  Register    the decision register with staleness alerts and a generated status block
  review      sprint review: three acceptance outcomes, the exception list, flow measures
  gate_check  whether the items a gate depends on are accepted (acceptance of items is not the gate)
  lint_status refuses status text that turns sprint acceptance into a production claim
  bus_factor  key-person risk on both sides of the engagement
No model calls. Deterministic, standard library only (plus fieldkit.deployment.is_person).
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field

from .deployment import is_person

LAYER = "v1.6"
PRIORITIES = {"P0": "control and safety", "P1": "customer outcome",
              "P2": "reusable capability", "P3": "optimization"}
OUTCOMES = ("accepted", "accepted with follow-up", "not accepted")
GATES = ("Architecture Review", "Build Complete", "Shadow Exit", "Model-Risk Approval", "Live Stable")
_TESTABLE = re.compile(r"\d|\bexactly\b|\bno\b|\bnone\b|\bevery\b|\bonly\b|\brejects?\b|\breturns?\b", re.I)


@dataclass
class Item:
    key: str
    title: str
    priority: str
    points: int
    owner: str = ""                       # accountable owner who will accept it
    acceptance: list = field(default_factory=list)
    evidence: dict = field(default_factory=dict)   # criterion index -> evidence path
    gate: str = ""                        # the gate this item is entry evidence for, if any
    requested_by: str = ""
    status: str = "proposed"              # proposed | in sprint | done | <one of OUTCOMES>
    follow_up_day: int | None = None
    follow_up: str = ""
    blocked_days: int = 0

    def ready_problems(self) -> list[str]:
        p = []
        if self.priority not in PRIORITIES:
            p.append(f"priority {self.priority!r} is not P0-P3")
        if not is_person(self.owner):
            p.append("no named accountable owner")
        if not self.acceptance:
            p.append("no acceptance criteria")
        for i, c in enumerate(self.acceptance):
            if not _TESTABLE.search(c):
                p.append(f"criterion {i + 1} is not testable: {c!r}")
        return p

    @property
    def ready(self) -> bool:
        return not self.ready_problems()

    def done_problems(self) -> list[str]:
        return [f"criterion {i + 1} has no evidence" for i in range(len(self.acceptance))
                if not self.evidence.get(i)]

    @property
    def done(self) -> bool:
        return self.ready and not self.done_problems()

    @property
    def accepted(self) -> bool:
        return self.status in ("accepted", "accepted with follow-up")


@dataclass
class Plan:
    capacity: int
    selected: list
    deferred: list
    violations: list
    authorized_by: str = ""
    warnings: list = field(default_factory=list)

    @property
    def points(self) -> int:
        return sum(i.points for i in self.selected)


def rank(items):
    """The ordering rule. Stable within a priority (the backlog's own order breaks ties)."""
    return sorted(items, key=lambda i: i.priority)


def plan_sprint(items, capacity: int, pinned=(), authorized_by: str = "") -> Plan:
    """Fill the sprint in priority order. `pinned` keys are forced in first (a sponsor request).
    The guard: if any P3 item is selected while a Ready P0-P2 item is left out, that is a displacement.
    A displacement is allowed only when `authorized_by` names a decision record."""
    ready = [i for i in items if i.ready]
    chosen, used = [], 0
    for i in [x for x in ready if x.key in pinned] + [x for x in rank(ready) if x.key not in pinned]:
        if used + i.points <= capacity:
            chosen.append(i)
            used += i.points
    deferred = [i for i in rank(ready) if i not in chosen]
    violations = []
    for low in [c for c in chosen if c.priority == "P3"]:
        for high in [d for d in deferred if d.priority in ("P0", "P1", "P2")]:
            violations.append(f"{low.key} ({low.priority}, {low.points} pts) displaced {high.key} "
                              f"({high.priority} {PRIORITIES[high.priority]}, {high.points} pts)"
                              + (f"; entry evidence for {high.gate}" if high.gate else ""))
    if violations and authorized_by:
        violations = [v + f" [authorized by {authorized_by}]" for v in violations]
    warnings = [f"{d.key} (P0, {d.points} pts) deferred for capacity while lower-priority work is in: "
                f"split it or re-plan" for d in deferred
                if d.priority == "P0" and any(c.priority > "P0" for c in chosen)]
    return Plan(capacity, chosen, deferred, violations, authorized_by, warnings)


def gate_check(gate: str, items, day: int) -> tuple[bool, list[str]]:
    """Entry evidence for a gate: every item tagged with the gate must be accepted (with a follow-up only
    if the follow-up day is before the gate). Passing this check is necessary, never sufficient: the gate
    has its own owner and its own decision."""
    missing = []
    for i in items:
        if i.gate != gate:
            continue
        if not i.accepted:
            missing.append(f"{i.key} {i.title}: {i.status}")
        elif i.status == "accepted with follow-up" and (i.follow_up_day or 10**9) > day:
            missing.append(f"{i.key} {i.title}: follow-up due day {i.follow_up_day}")
    return (not missing, missing)


@dataclass
class Record:
    key: str
    question: str
    owner: str
    raised_day: int
    due_day: int | None = None
    kind: str = "design"            # design | access | scope change | acceptance | stop
    options: list = field(default_factory=list)
    status: str = "open"            # open | decided | dropped
    decision: str = ""
    decided_day: int | None = None
    evidence: str = ""
    impact: str = ""                # milestone impact, in days or gate terms

    def age(self, today: int) -> int:
        return (self.decided_day if self.decided_day is not None else today) - self.raised_day


class Register:
    """The decision register. Alerts are the point: a register nobody is alerted by is a list."""

    def __init__(self, customer: str, stale_after: int = 14):
        self.customer, self.stale_after, self.records = customer, stale_after, {}

    def add(self, r: Record) -> Record:
        self.records[r.key] = r
        return r

    def decide(self, key: str, decision: str, day: int, evidence: str = "", impact: str = ""):
        r = self.records[key]
        r.status, r.decision, r.decided_day = "decided", decision, day
        r.evidence, r.impact = evidence or r.evidence, impact or r.impact
        return r

    def alerts(self, today: int) -> list[tuple[str, str, str]]:
        out = []
        for r in self.records.values():
            if not is_person(r.owner):
                out.append((r.key, "NO OWNER", f"owner {r.owner!r} is not a named person"))
            if r.status == "open":
                if r.due_day is None:
                    out.append((r.key, "NO DUE DAY", "open with no due day"))
                elif today > r.due_day:
                    out.append((r.key, "OVERDUE", f"{today - r.due_day} days past due (day {r.due_day}), "
                                                  f"{r.owner}"))
                elif r.age(today) >= self.stale_after:
                    out.append((r.key, "STALE", f"open {r.age(today)} days, due day {r.due_day}"))
                if r.kind == "scope change" and not r.impact:
                    out.append((r.key, "NO IMPACT", "scope change without a milestone impact"))
            if r.status == "decided" and not r.evidence:
                out.append((r.key, "NO EVIDENCE", "decided with nothing attached"))
        return out

    def status(self, today: int) -> str:
        rs = list(self.records.values())
        open_ = [r for r in rs if r.status == "open"]
        lines = [f"DECISIONS  {self.customer}  day {today}",
                 f"{'key':<10}{'kind':<14}{'owner':<20}{'age':>4}  {'due':>4}  state"]
        for r in sorted(rs, key=lambda r: (r.status != "open", -(r.age(today)))):
            state = r.status if r.status != "open" else (
                "OVERDUE" if r.due_day is not None and today > r.due_day else "open")
            lines.append(f"{r.key:<10}{r.kind:<14}{r.owner:<20}{r.age(today):>4}  "
                         f"{(r.due_day if r.due_day is not None else '-'):>4}  {state}")
        a = self.alerts(today)
        oldest = max(open_, key=lambda r: r.age(today)) if open_ else None
        lines.append(f"open: {len(open_)}  decided: {sum(r.status == 'decided' for r in rs)}  alerts: {len(a)}"
                     + (f"  oldest open: {oldest.key} ({oldest.age(today)} days, {oldest.owner})" if oldest else ""))
        for k, kind, msg in a:
            lines.append(f"  ALERT {kind:<12}{k:<10}{msg}")
        return "\n".join(lines)


@dataclass
class Review:
    sprint: str
    committed: int
    accepted_points: int
    outcomes: dict
    exceptions: list
    carried: list
    blocked_days: int

    @property
    def goal_share(self) -> float:
        return self.accepted_points / self.committed if self.committed else 0.0


def review(sprint: str, items, day: int) -> Review:
    """Day-10 review. Every item gets one of the three outcomes; nothing is 'mostly done'.
    The exception list holds every P0 item not accepted and every dated follow-up."""
    outcomes = {o: [] for o in OUTCOMES}
    exceptions, carried = [], []
    for i in items:
        if i.status not in OUTCOMES:
            i.status = "not accepted"
        if i.status == "accepted" and not i.done:
            i.status = "not accepted"          # acceptance needs evidence; a demo is not evidence
        outcomes[i.status].append(i)
        if i.status == "not accepted":
            carried.append(i)
            if i.priority == "P0":
                exceptions.append((i.key, i.owner, "control item not accepted", i.gate or "-"))
        if i.status == "accepted with follow-up":
            if i.follow_up_day is None:
                i.status = "not accepted"      # a follow-up without a date is a 'no'
                outcomes["accepted with follow-up"].remove(i)
                outcomes["not accepted"].append(i)
                carried.append(i)
            else:
                exceptions.append((i.key, i.owner, f"follow-up by day {i.follow_up_day}: {i.follow_up}",
                                   i.gate or "-"))
    committed = sum(i.points for i in items)
    acc = sum(i.points for i in items if i.accepted)
    return Review(sprint, committed, acc, outcomes, exceptions, carried, sum(i.blocked_days for i in items))


_PROD_CLAIM = re.compile(r"\b(approved for production|production[- ]ready|ready for production|go[- ]live approved|"
                         r"signed off for (?:production|release))\b", re.I)


def lint_status(text: str, gates_passed: dict) -> list[str]:
    """Sprint acceptance is not production approval. Flag any production claim in a status report
    unless the gate that grants it has actually passed."""
    problems = []
    for m in _PROD_CLAIM.finditer(text):
        if not gates_passed.get("Model-Risk Approval") and not gates_passed.get("Live Stable"):
            problems.append(f"production claim {m.group(0)!r} with gates passed "
                            f"{sum(bool(v) for v in gates_passed.values())} of {len(GATES)}")
    return problems


def bus_factor(holdings: dict) -> list[str]:
    """holdings: capability -> list of (person, side). Flags single holders and people who hold three or more."""
    flags, count = [], {}
    for cap, holders in holdings.items():
        for person, side in holders:
            count[(person, side)] = count.get((person, side), 0) + 1
        if len(holders) == 1:
            p, s = holders[0]
            flags.append(f"single holder: {cap} -> {p} ({s})")
    for (p, s), n in sorted(count.items(), key=lambda kv: -kv[1]):
        if n >= 3:
            flags.append(f"concentration: {p} ({s}) holds {n} of {len(holdings)} capabilities")
    return flags
