"""The weekly status that tells the truth: seven parts, a lint, and a computed color.

Reuses fieldkit.cadence.lint_status for the production-claim rule (acceptance is not approval)."""
import re
import _path  # noqa: F401
from dataclasses import dataclass, field
from fieldkit.cadence import lint_status, GATES

PARTS = ("headline", "done", "in_progress", "blockers", "risks", "decisions", "next_week")


@dataclass
class Blocker:
    text: str
    owner: str
    since: int          # engagement day it became a blocker
    due: int | None     # day a decision or action is promised


@dataclass
class Status:
    week: int
    day: int
    reported: str                    # green | amber | red, as the author chose it
    committed_pilot: int
    forecast_pilot: int
    headline: str = ""
    done: list = field(default_factory=list)
    in_progress: list = field(default_factory=list)
    blockers: list = field(default_factory=list)
    risks: list = field(default_factory=list)
    decisions: list = field(default_factory=list)   # (decision, owner, due day)
    next_week: list = field(default_factory=list)
    gates_passed: dict = field(default_factory=dict)


def computed_color(s):
    slip = s.forecast_pilot - s.committed_pilot
    oldest = max((s.day - b.since for b in s.blockers), default=0)
    if oldest > 21 or slip > 14:
        return "red"
    if oldest > 10 or slip > 0:
        return "amber"
    return "green"


def lint(s):
    p = []
    for part in PARTS:
        v = getattr(s, part)
        if not v:
            p.append(f"missing part: {part}")
    slip = s.forecast_pilot - s.committed_pilot
    if slip > 0 and not re.search(r"\b(slip|slips|moves|late)\b", s.headline, re.I):
        p.append(f"headline hides a slip of {slip} days (pilot day {s.committed_pilot} -> {s.forecast_pilot})")
    for b in s.blockers:
        if not b.owner:
            p.append(f"blocker without an owner: {b.text}")
        if b.due is None:
            p.append(f"blocker without a date: {b.text}")
    for d in s.decisions:
        if len(d) < 3 or not d[1] or d[2] is None:
            p.append(f"decision without owner and date: {d[0]}")
    c = computed_color(s)
    order = {"green": 0, "amber": 1, "red": 2}
    if order[s.reported] < order[c]:
        p.append(f"reported {s.reported}, computed {c}")
    text = " ".join([s.headline] + s.done + s.in_progress)
    p += lint_status(text, s.gates_passed)
    n = sum(bool(v) for v in s.gates_passed.values())
    if not re.search(r"gates passed \d of 5", text):
        p.append(f"no gates line (gates passed {n} of 5)")
    return p


def render(s):
    out = [f"Greystone weekly status, week {s.week} (day {s.day})  [{computed_color(s)}]", f"HEADLINE  {s.headline}"]
    for label, items in (("DONE", s.done), ("IN PROGRESS", s.in_progress)):
        out.append(label); out += [f"  - {x}" for x in items]
    out.append("BLOCKERS"); out += [f"  - {b.text} (owner {b.owner or '?'}, open {s.day - b.since} days, due {f"day {b.due}" if b.due else "no date"})" for b in s.blockers]
    out.append("RISKS"); out += [f"  - {x}" for x in s.risks]
    out.append("DECISIONS NEEDED"); out += [f"  - {d[0]} (owner {d[1]}, by day {d[2]})" for d in s.decisions]
    out.append("NEXT WEEK"); out += [f"  - {x}" for x in s.next_week]
    return "\n".join(out)


GATES0 = {g: False for g in GATES}
SUB = Blocker("Production subscription approval", "Sam Oakley", 3, 47)
SAMPLE = Blocker("Data sample request has no named owner", "", 10, None)

DRAFT_W6 = Status(6, 40, "green", 140, 146,
    headline="On track; security review is the only open item and the sprint was accepted, production-ready by pilot",
    done=["Sprint 2 accepted by Michael Hart"], in_progress=["Prior-authorization drafter on synthetic referrals"],
    blockers=[SUB, SAMPLE], risks=[], decisions=[], next_week=["Sprint 3"], gates_passed=GATES0)

HONEST_W6 = Status(6, 40, "red", 140, 146,
    headline="Pilot slips from day 140 to day 146 unless the subscription is approved by day 47; gates passed 0 of 5",
    done=["Sprint 2 accepted by Michael Hart (acceptance, not approval)", "Security clinic 4: 11 of 41 questions closed"],
    in_progress=["Prior-authorization drafter on synthetic referrals", "Answers to Sam Oakley's 30 open questions"],
    blockers=[Blocker("Northlight owes the subscription onboarding answers", "Callum Reid", 6, 47),
              Blocker("Data sample request: owner named today", "Denise Alvarez", 10, 54)],
    risks=["Downtown coordinators have not seen a draft since day 19; adoption risk at two clinics"],
    decisions=[("Fax path: in or out of pilot", "Denise Alvarez", 44)],
    next_week=["Send onboarding answers by day 47", "Shadow the downtown queue with Luis Ortega"],
    gates_passed=GATES0)

# Ten weeks of what was reported against what the rule computes (oldest blocker age, forecast slip).
SERIES = [  # week, day, reported, oldest blocker since, forecast
    (1, 7, "green", 3, 140), (2, 14, "green", 3, 140), (3, 21, "green", 3, 140), (4, 28, "green", 3, 140),
    (5, 35, "green", 3, 144), (6, 40, "green", 3, 146), (7, 49, "amber", 3, 146), (8, 56, "amber", 3, 148),
    (9, 63, "red", 3, 146), (10, 70, "red", 3, 144),
]

def series():
    rows = []
    for w, d, rep, since, fc in SERIES:
        s = Status(w, d, rep, 140, fc, blockers=[Blocker("x", "o", since, d + 7)] if d - since > 0 else [])
        rows.append((w, d, rep, computed_color(s), fc))
    return rows
