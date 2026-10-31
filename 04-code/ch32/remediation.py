"""Remediation: findings close only with retest evidence; burn-down from day 103."""
import _paths  # noqa: F401
from fieldkit.security import RemediationPlan
from world import findings, CLOSURES, PLANNED

fs = {f.id: f for f in findings()}
plan = RemediationPlan(list(fs.values()))
try:
    fs["F-08"].close(106, "")
except ValueError as e:
    print(f"day 106, F-08 fix deployed, close attempted: {e}")
for fid, day, ev in CLOSURES:
    fs[fid].close(day, ev)
print("closed with retest evidence:")
for fid, day, ev in CLOSURES:
    print(f"  {fid} day {day}: {ev}")
print("open on day 112: " + ", ".join(f"{f.id} ({f.severity}, due {f.due_day})" for f in plan.open_on(112)))
print("compensating controls on open high findings:")
for f in plan.open_on(112):
    if f.severity == "high":
        print(f"  {f.id}: {f.compensating}")
print("burn-down: " + "  ".join(f"d{d} {n}" for d, n in plan.burndown([103, 104, 105, 108, 111, 112])))
for fid, day in PLANNED:
    fs[fid].close(day, "planned")
print("plan if every retest lands on its date: " + "  ".join(
    f"d{d} {n}" for d, n in plan.burndown([112, 114, 115, 117, 120, 125, 128])))
