"""Escalation with dates (fieldkit v2, Chapter 15).

An access request that has waited longer than the agreed response time is escalated one level at a
time, always with a date, always with the owner copied, and only when the next move is the
customer's. The output is a dated ask, never a complaint:

    level 1  dated ask to the owner
    level 2  the sponsor, owner copied (or the steering forum if the owner is the sponsor)
    level 3  an item on the steering agenda, owner and sponsor present

Rules, in the order they are applied:
  1. the ball must be on the customer's side; if the next action is ours, the output is our own task
  2. a request must have waited the agreed response time for its rung, or the work it blocks must be
     planned to start within the warning window
  3. no level is skipped: the recommended level is at most one above the last level sent
  4. every note states what is blocked, the plan day it was due to start, the days it has already
     cost, one ask and the date by which the ask is needed
"""
from dataclasses import dataclass, field
from typing import Optional

from .access import LADDER

DEFAULT_SLA = {"synthetic": 10, "sampled": 21, "shadowed": 30, "live": 30}
LEVEL_NAMES = {0: "none", 1: "dated ask to owner", 2: "sponsor, owner copied", 3: "steering agenda item"}


@dataclass
class Escalation:
    key: str
    level: int
    day: int
    days_open: int
    sla: int
    to: str
    copied: list
    blocks: list            # (work item, planned start day, days late)
    ask: str
    ask_by: int
    reason: str
    customer: str = ""
    what: str = ""
    waiting_on: str = ""
    customer_days: int = 0
    label: str = ""

    def note(self) -> str:
        lines = [f"ESCALATION  level {self.level} ({self.label or LEVEL_NAMES[self.level]})  {self.customer}  day {self.day}",
                 f"request:      {self.key} ({self.what})",
                 f"waiting:      {_days(self.customer_days)} on {self.waiting_on}; agreed response time {self.sla} days"
                 + (f" ({self.days_open} days open, {self.days_open - self.customer_days} of them on our side)"
                    if self.days_open != self.customer_days else ""),
                 "blocks:       " + "; ".join(
                     f"{w} (planned day {s}, " + (f"{_days(late)} late)" if late > 0 else f"starts costing in {_days(-late)})")
                     for w, s, late in self.blocks) if self.blocks else "blocks:       nothing planned yet",
                 f"ask:          {self.ask} by day {self.ask_by}",
                 f"to:           {self.to}" + (f"   copied: {', '.join(self.copied)}" if self.copied else ""),
                 f"if not by day {self.ask_by}: level {min(3, self.level + 1)} ({LEVEL_NAMES[min(3, self.level + 1)]})"]
        return "\n".join(lines)


@dataclass
class EscalationPolicy:
    sponsor: str
    steering: str
    sla: dict = field(default_factory=lambda: dict(DEFAULT_SLA))
    warning_days: int = 3          # blocked work planned to start within this window triggers level 1
    answer_days: int = 5           # how long each ask allows before the next level
    plan: dict = field(default_factory=dict)      # work item -> planned start day
    asks: dict = field(default_factory=dict)      # request key -> the specific ask
    sent: dict = field(default_factory=dict)      # request key -> list of (day, level, to)

    def record(self, key: str, day: int, level: int, to: str) -> None:
        self.sent.setdefault(key, []).append((day, level, to))

    def last_level(self, key: str) -> int:
        return max((lvl for _, lvl, _ in self.sent.get(key, [])), default=0)

    def last_valid_level(self, key: str, tracker) -> int:
        """Highest level sent that followed the rules; a skipped or premature level does not count."""
        r, prev = tracker.requests[key], 0
        for day, lvl, _ in sorted(self.sent.get(key, [])):
            if lvl <= prev + 1 and _ball_on(r, day) == "customer":
                prev = max(prev, lvl)
        return prev

    def ask_by(self, req, today):
        """The answer is needed by the earlier of the answer window and the next planned start."""
        upcoming = [s for _, s, late in self.blocked_work(req, today) if late < 0]
        return min([today + self.answer_days] + upcoming)

    def blocked_work(self, req, today):
        out = []
        for w in req.blocks:
            start = self.plan.get(w)
            if start is not None:
                out.append((w, start, today - start))
        return sorted(out, key=lambda x: x[1])

    def rule_level(self, req, today) -> tuple:
        d = customer_days(req, today)
        sla = self.sla[req.rung]
        blocked = self.blocked_work(req, today)
        late = max((x[2] for x in blocked), default=None)
        if d >= 2 * sla and late is not None and late > 0:
            return 3, f"{_days(d)} on the customer's side, twice the agreed {sla}, and planned work is {_days(late)} late"
        if d >= sla + 14 and late is not None and late > -self.warning_days:
            return 2, f"{_days(d)} on the customer's side, two weeks past the agreed {sla}, and blocking planned work"
        if d >= sla:
            return 1, f"{_days(d)} on the customer's side against an agreed {sla}"
        if late is not None and late >= -self.warning_days:
            return 1, f"blocked work starts within {self.warning_days} days"
        return 0, f"{_days(d)} on the customer's side; agreed {sla}; level 1 due day {today + sla - d}"

    def route(self, level: int, owner: str) -> tuple:
        if level == 1:
            return owner, []
        if level == 2 and self.sponsor != owner:
            return self.sponsor, [owner]
        return self.steering, [owner] + ([self.sponsor] if self.sponsor != owner else [])

    def review(self, tracker, today):
        """Return (escalations, our_tasks, quiet) for every open request."""
        escalations, ours, quiet = [], [], []
        for r in tracker.waiting(today):
            if getattr(r, "ball", "customer") == "us":
                ours.append(f"OUR MOVE  {r.key}: {r.next_action} (open {r.days_open(today)} days; not escalated)")
                continue
            lvl, why = self.rule_level(r, today)
            if lvl == 0:
                quiet.append(f"quiet     {r.key}: {why}")
                continue
            capped = min(lvl, self.last_valid_level(r.key, tracker) + 1)
            if capped < lvl:
                why += f"; capped at level {capped} because level {capped} has not been sent"
            to, copied = self.route(capped, r.owner)
            label = LEVEL_NAMES[capped] if not (capped == 2 and self.sponsor == r.owner) else \
                "owner is the sponsor: steering, owner copied"
            escalations.append(Escalation(
                key=r.key, level=capped, day=today, days_open=r.days_open(today), sla=self.sla[r.rung],
                to=to, copied=copied, blocks=self.blocked_work(r, today),
                ask=self.asks.get(r.key, r.next_action or "a decision"), ask_by=self.ask_by(r, today),
                reason=why, customer=tracker.customer, what=r.what,
                waiting_on=f"{r.owner} / {r.next_action}" if r.next_action else r.owner,
                customer_days=customer_days(r, today), label=label))
        return escalations, ours, quiet

    def audit(self, tracker):
        """Check the record of escalations already sent against the rules."""
        findings = []
        for key, items in self.sent.items():
            r = tracker.requests[key]
            prev = 0
            for day, lvl, to in sorted(items):
                if lvl > prev + 1:
                    findings.append(f"day {day}: {key} level {lvl} sent to {to} with no level {prev + 1} on record")
                ball = _ball_on(r, day)
                if ball == "us":
                    findings.append(f"day {day}: {key} escalated while the next action was ours")
                prev = max(prev, lvl)
        return findings


def _days(n):
    return f"{n} day" + ("" if abs(n) == 1 else "s")


def customer_days(req, today):
    """Days the request has waited with the next move on the customer's side."""
    if req.requested_day is None:
        return 0
    end = req.granted_day if req.status == "granted" else today
    hist = getattr(req, "ball_history", None) or [(req.requested_day, getattr(req, "ball", "customer"))]
    total = 0
    for i, (d, ball) in enumerate(hist):
        stop = hist[i + 1][0] if i + 1 < len(hist) else end
        if ball == "customer":
            total += max(0, min(stop, end) - max(d, req.requested_day))
    return total


def _ball_on(req, day):
    hist = getattr(req, "ball_history", None)
    if not hist:
        return getattr(req, "ball", "customer")
    ball = "customer"
    for d, b in hist:
        if d <= day:
            ball = b
    return ball
