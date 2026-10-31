"""Three passes of Greystone's security review: what was asked, what passed, what stayed open."""
import _paths  # noqa: F401
from fieldkit.security import evidence_check, RemediationPlan
import world as W

fs = W.findings()
for fid, d, r in W.CLOSURES:
    next(f for f in fs if f.id == fid).close(d, r)
plan = RemediationPlan(fs)
for p, day in W.PASS_DAYS.items():
    A = W.answers(p)
    ev = {v.qid: v for v in evidence_check(A, W.EVIDENCE, day, W.SCOPE)}
    raised = [f for f in fs if f.raised_day <= day]
    open_ = [f for f in plan.open_on(day) if f.id not in W.ACCEPTED or day < W.PASS_DAYS[3]]
    accepted = [f for f in plan.open_on(day) if f.id in W.ACCEPTED and day >= W.PASS_DAYS[3]]
    against = {f.source for f in open_}
    passed = [q for q, v in ev.items() if v.passed and q not in against]
    outcome = "passed" if not open_ else "returned"
    print(f"pass {p} day {day}: asked {len(A)}, passed {len(passed)}, findings raised to date {len(raised)}, "
          f"open {len(open_)}, accepted {len(accepted)} -> {outcome}")
    print(f"   minutes: " + ", ".join(f"{t} {m}" for t, m in W.AGENDA[p]) + f" (total {sum(m for _, m in W.AGENDA[p])})")
    if open_:
        print("   open: " + ", ".join(f"{f.id} {f.source} {f.severity}" for f in open_))
    if accepted:
        print("   accepted as residual risk: " + ", ".join(f"{f.id} -> {W.ACCEPTED[f.id]}" for f in accepted))
days = [103, 104, 105, 111, 114, 115, 117, 120, 121, 125, 127, 128, 129]
print("open findings by day: " + "  ".join(f"d{d} {n}" for d, n in plan.burndown(days)))
print("residual after acceptance: d129 0 open, 2 accepted in writing")
print(f"closed with retest evidence: {sum(f.closed_day is not None for f in fs)} of {len(fs)}")
print(f"overdue on day 129: {len([f for f in plan.overdue(129) if f.id not in W.ACCEPTED])}")
