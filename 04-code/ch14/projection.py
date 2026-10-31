"""Chapter 14: days-to-pilot projection from gate days, calendars and build effort.

Pilot means draft-only shadow on live referrals at two clinics (question M18). The projection is a critical path:

    data day   = max(Architecture Review day, privacy board meeting day) + managed-service provider change days
    build done = scope day + calendar days to spend the build effort at the team's build fraction
    pilot day  = max(data day, build done) + evaluation and clinical sign-off days

Every input carries a claim strip (measured, estimated, assumed) and a source, so the date can be audited.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, replace

from decision_tree import CLASSES, classify

EFFORT = {CLASSES[0]: 2, CLASSES[1]: 4, CLASSES[2]: 6, CLASSES[3]: 8}   # engineer-days per step (estimated)
RATE, CAP = 260, 450_000


@dataclass(frozen=True)
class Inputs:
    scope_day: int = 19                 # measured: the day the scope is signed
    arch_review_day: int = 94           # estimated: Sam Oakley's next slot, Ch2 field estimate [CHECK ch02]
    board_meeting_day: int = 75         # measured: board calendar; submission complete by day 65
    board_submission_day: int = 63      # proposed design: our submission date
    board_lead_days: int = 10           # measured: complete submissions ten days ahead
    board_cycle_days: int = 28          # measured: monthly
    msp_change_days: int = 18           # vendor position: managed-service provider estimate
    eval_days: int = 28                 # proposed design: evaluation on the sample and clinical sign-off
    fdes: int = 2                       # measured: staffing
    build_fraction: float = 0.65        # assumed: share of an FDE week left for building after meetings and access work


STRIP = dict(scope_day="measured", arch_review_day="estimated", board_meeting_day="measured",
             board_submission_day="assumed", board_lead_days="measured", board_cycle_days="measured",
             msp_change_days="estimated", eval_days="assumed", fdes="measured", build_fraction="assumed")


def effort(steps) -> int:
    return sum(EFFORT[classify(s)] for s in steps)


def board_day(i: Inputs) -> int:
    meet = i.board_meeting_day
    while i.board_submission_day > meet - i.board_lead_days:
        meet += i.board_cycle_days
    return meet


def project(steps, i: Inputs = Inputs()) -> dict:
    e = effort(steps)
    working = e / (i.fdes * i.build_fraction)
    build_done = i.scope_day + math.ceil(working * 7 / 5)
    board = board_day(i)
    data = max(i.arch_review_day, board) + i.msp_change_days
    pilot = max(data, build_done) + i.eval_days
    critical = "data" if data >= build_done else "build"
    hours = e * 8
    return dict(effort_days=e, build_done=build_done, board=board, data=data, pilot=pilot, critical=critical,
                slack=abs(data - build_done), hours=hours, cost=hours * RATE, headroom=CAP - hours * RATE)


def with_(i: Inputs = Inputs(), **kw) -> Inputs:
    return replace(i, **kw)
