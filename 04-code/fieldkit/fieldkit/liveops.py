"""fieldkit.liveops (v5.1, Chapter 42; package stays 0.1.0): the first ninety days in production.

Seven small pieces, each born from a failure in Chapter 42's ninety-day replay at Pennant:
  DriftMonitor     a leading signal (PSI on an input feature) and a lagging one (scored match rate), each with an
                   owner on the customer side and a read log; a monitor nobody reads is reported as not running.
  recalibrate      a proceed threshold re-fit on a production sample so the silently-wrong upper bound stays
                   under the customer's line; returns a record that needs a signature before it applies.
  PageRoute        who is paged, in what order, and who approves rollback; a vendor address as primary, or a
                   person (not a role with a deputy) as rollback approver, is a finding.
  Incident         a timeline of minute-stamped events with time to detect, acknowledge and mitigate.
  deprecation_plan a provider retirement read against the customer's change freezes: the last safe change day,
                   whether a freeze exception is needed, and by when the gate evidence must exist.
  upgrade_gate     PROMOTE / HOLD / ROLLBACK over named dimensions; lost critical items need an owner's sign-off.
  OwnershipMap     the five ownership proofs plus operational holdings, holders and deputies: the two-of-five rule,
                   single points with no deputy, orphans when a holder leaves, a coverage share. Hand-over
                   readiness itself stays Chapter 41's handover.score, re-run on production evidence.
  live_stable      the ninety-day review as the Live Stable gate: every criterion with evidence and who measured it.
Pure Python, deterministic, no model calls.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from .synthetic import psi as _psi
from .evals import wilson

VENDOR_DOMAINS = ("northlight.example",)


# ---------------------------------------------------------------- drift
@dataclass
class DriftMonitor:
    leading_owner: str
    lagging_owner: str
    psi_alarm: float = 0.20
    match_floor: float = 0.80
    reads: list = field(default_factory=list)      # (day, reader)

    def leading(self, baseline: list, window: list) -> float:
        return _psi(baseline, window)

    def check(self, day: int, baseline: list, window: list, matched: int | None = None, scored: int | None = None):
        """Returns a list of alarms for this day; the lagging check runs only on days a scored sample exists."""
        out = []
        p = self.leading(baseline, window)
        if p >= self.psi_alarm:
            out.append(("leading", day, round(p, 3), self.leading_owner))
        if scored:
            lo, _ = wilson(matched, scored)
            if matched / scored < self.match_floor:
                out.append(("lagging", day, round(matched / scored, 3), self.lagging_owner))
        return out

    def read(self, day: int, reader: str):
        self.reads.append((day, reader))

    def running(self, today: int, max_gap: int = 8) -> tuple[bool, str]:
        """A monitor counts as running only if a customer person read it within max_gap days."""
        cust = [d for d, r in self.reads if not any(v in r for v in VENDOR_DOMAINS) and r != "Northlight"]
        if not cust:
            return False, "never read by a customer person"
        gap = today - max(cust)
        return (gap <= max_gap), f"last customer read {gap} days ago"


# ---------------------------------------------------------------- re-calibration
def recalibrate(sample: list[tuple[float, bool]], max_wrong_upper: float, owner: str, grid=None) -> dict:
    """sample: (confidence, correct) pairs from a scored production sample. Picks the lowest threshold whose
    proceed set keeps the Wilson upper bound on silently wrong (proceeded and incorrect) at or below the line."""
    grid = grid or [round(0.50 + 0.01 * i, 2) for i in range(50)]
    for t in grid:
        go = [ok for c, ok in sample if c >= t]
        if not go:
            continue
        wrong = sum(1 for ok in go if not ok)
        _, hi = wilson(wrong, len(go))
        if hi <= max_wrong_upper:
            return dict(threshold=t, proceed=len(go), of=len(sample), wrong=wrong, wrong_upper=round(hi, 4),
                        owner=owner, signed=False, status="needs signature")
    return dict(threshold=None, proceed=0, of=len(sample), wrong=0, wrong_upper=None, owner=owner,
                signed=False, status="no threshold meets the line: route everything")


# ---------------------------------------------------------------- paging
@dataclass
class PageRoute:
    primary: str
    secondary: str
    rollback_approver: str          # a role, resolved through the ownership map
    approver_is_role: bool = True

    def lint(self, ownership: "OwnershipMap | None" = None) -> list[str]:
        f = []
        if any(v in self.primary for v in VENDOR_DOMAINS):
            f.append(f"primary page goes to a vendor address: {self.primary}")
        if not self.approver_is_role:
            f.append(f"rollback approver is a person, not a role with a deputy: {self.rollback_approver}")
        if ownership is not None and self.approver_is_role:
            h = ownership.holdings.get(self.rollback_approver)
            if not h or h.holder in ownership.departed:
                f.append(f"rollback approver role {self.rollback_approver} has no present holder")
            elif not h.deputy:
                f.append(f"rollback approver role {self.rollback_approver} has no deputy")
        return f


# ---------------------------------------------------------------- incidents
def hhmm(m: int) -> str:
    return f"{m // 60:02d}:{m % 60:02d}"


@dataclass
class Incident:
    name: str
    events: list = field(default_factory=list)      # (minute of day, kind, text)

    def log(self, minute: int, kind: str, text: str):
        self.events.append((minute, kind, text))

    def first(self, kind):
        xs = [m for m, k, _ in self.events if k == kind]
        return min(xs) if xs else None

    def metrics(self) -> dict:
        s, d, a, m = (self.first(k) for k in ("start", "detect", "ack", "mitigate"))
        return dict(ttd=None if None in (s, d) else d - s, tta=None if None in (d, a) else a - d,
                    ttm=None if None in (s, m) else m - s)


# ---------------------------------------------------------------- deprecation under a freeze
def deprecation_plan(notice_day: int, retire_day: int, freezes: list[tuple[int, int]], evidence_days: int,
                     read_day: int | None = None) -> dict:
    """Days are integers on one calendar. evidence_days: days to produce the upgrade gate's evidence."""
    read = notice_day if read_day is None else read_day
    frozen = lambda d: any(a <= d <= b for a, b in freezes)
    in_freeze = frozen(retire_day)
    earliest_ready = read + evidence_days
    last_safe = max((d for d in range(read, retire_day) if not frozen(d)), default=None)
    if last_safe is not None and earliest_ready <= last_safe:
        action = f"change in a normal window by day {last_safe}"
        exception = False
    elif earliest_ready < retire_day:
        action = f"freeze exception: evidence by day {earliest_ready}, change before day {retire_day}"
        exception = True
    else:
        action = f"cannot be ready before retirement on day {retire_day}: plan the outage or a fallback route"
        exception = True
    return dict(notice=notice_day, read=read, retire=retire_day, retire_in_freeze=in_freeze,
                last_safe_normal_day=last_safe, earliest_ready=earliest_ready, freeze_exception=exception,
                action=action, slack_days=((last_safe if not exception else retire_day - 1) - earliest_ready))


# ---------------------------------------------------------------- upgrade gate
def upgrade_gate(dims: dict, lost_critical: int, signoff: str | None = None,
                 accepted: dict | None = None) -> tuple[str, list[str]]:
    """dims: name -> (candidate, incumbent, floor, higher_is_better). ROLLBACK if any dimension misses its floor.
    HOLD if any dimension is worse than the incumbent (inside its floor) without a named person accepting it, or if
    lost critical items have no owner's sign-off. Otherwise PROMOTE."""
    why, verdict = [], "PROMOTE"
    accepted = accepted or {}
    for name, (cand, inc, floor, hib) in dims.items():
        ok_floor = cand >= floor if hib else cand <= floor
        if not ok_floor:
            why.append(f"{name}: {cand} misses floor {floor}")
            verdict = "ROLLBACK"
        elif (cand < inc) if hib else (cand > inc):
            if name in accepted:
                why.append(f"{name}: {cand} worse than incumbent {inc}, inside floor {floor}; accepted by {accepted[name]}")
            else:
                why.append(f"{name}: {cand} worse than incumbent {inc}")
                if verdict == "PROMOTE":
                    verdict = "HOLD"
    if lost_critical and not signoff:
        why.append(f"{lost_critical} lost critical items without an owner's sign-off")
        if verdict == "PROMOTE":
            verdict = "HOLD"
    return verdict, why


# ---------------------------------------------------------------- ownership and readiness
PROOFS = ("own-exec", "own-gold-set", "own-operations", "own-model-risk", "own-override")


@dataclass
class Holding:
    item: str
    holder: str | None
    deputy: str | None = None
    exercised: bool = False          # the holder (or deputy) has done it alone, with a record

    def score(self, departed: set) -> float:
        h = self.holder if self.holder not in departed else None
        if h is None and self.deputy and self.deputy not in departed:
            return 0.5               # the deputy inherits, but has no deputy of their own yet
        if h is None or h == "Northlight":
            return 0.0
        dep = self.deputy if self.deputy not in departed else None
        return 1.0 if (dep and self.exercised) else 0.5


@dataclass
class OwnershipMap:
    holdings: dict = field(default_factory=dict)
    departed: set = field(default_factory=set)

    def add(self, item, holder, deputy=None, exercised=False):
        self.holdings[item] = Holding(item, holder, deputy, exercised)

    def leave(self, person: str):
        self.departed.add(person)

    def coverage(self) -> float:
        return round(sum(h.score(self.departed) for h in self.holdings.values()) / len(self.holdings), 2)

    def two_of_five(self) -> list[str]:
        """No one holds more than two of the five ownership proofs without a named deputy on the extras."""
        out, by = [], {}
        for p in PROOFS:
            h = self.holdings.get(p)
            if h and h.holder and h.holder not in self.departed:
                by.setdefault(h.holder, []).append(h)
        for person, hs in by.items():
            bare = [h.item for h in hs if not h.deputy]
            if len(hs) > 2 and len(hs) - len([h for h in hs if h.deputy]) > 2:
                out.append(f"{person} holds {len(hs)} proofs, {len(bare)} without a deputy")
        return out

    def single_points(self) -> list[str]:
        """Every holding, proof or not, with no deputy: the v5.1 extension of the rule."""
        return [f"{h.item} -> {h.holder}" for h in self.holdings.values()
                if h.holder and h.holder not in self.departed and not h.deputy]

    def orphans(self) -> list[str]:
        return [h.item for h in self.holdings.values()
                if (h.holder in self.departed or h.holder is None) and not (h.deputy and h.deputy not in self.departed)]


# ---------------------------------------------------------------- the Live Stable gate
def live_stable(criteria: list[tuple[str, bool, str, str]]) -> tuple[str, list[str]]:
    """criteria: (name, met, evidence, measured_by). A criterion with no evidence or measured by the vendor alone
    does not count as met."""
    lines, ok = [], True
    for name, met, ev, by in criteria:
        counted = met and bool(ev) and by not in ("", "Northlight")
        ok &= counted
        lines.append(f"{'met ' if counted else 'OPEN'}  {name:<47} {ev}  [{by or 'nobody'}]")
    return ("LIVE STABLE" if ok else "NOT YET"), lines
