"""Triage the red team's twenty-item report the evening of day 127: one disposition per item, findings for the rest."""
import sys
import _paths  # noqa: F401
from collections import Counter
from fieldkit.redteam import triage, triage_lint, severity
from fieldkit.security import RemediationPlan
import world as W

items = W.report_items()
if "--naive" in sys.argv:
    print("NAIVE  every report item becomes a finding at the severity the report gave it")
    c = Counter(W.REPORTED_SEVERITY.values())
    print(f"findings: {len(items)}   " + "  ".join(f"{k} {c[k]}" for k in ("critical", "high", "medium", "low")))
    print(f"owners named in the report: 0 of {len(items)}   items sharing a root with another item: "
          f"{sum(1 for i in items if [j.root for j in items].count(i.root) > 1)}")
    raise SystemExit
disp, new = triage(items, W.OPEN_ROOTS, W.OWNERS, W.SOURCES, W.TRIAGE_DAY, 13, compensating=W.COMPENSATING)
print(f"TRIAGE  day {W.TRIAGE_DAY}, 18:10 to 19:25  Sam Oakley, Jordan Pike, Sofia Brennan, Callum Reid")
for d, it in zip(disp, items):
    print(f"{it.id}  {it.title[:52]:<52} {d.disposition:<12} {d.target:<16} {d.reason}")
c = Counter(d.disposition for d in disp)
print("dispositions: " + ", ".join(f"{k} {v}" for k, v in c.items()))
print(f"lint: {'; '.join(triage_lint(disp, items)) or 'every item has exactly one disposition'}")
print("SEVERITY  likelihood x impact, high 12 and above, medium 6 to 11, low 5 and below")
for f in new:
    it = next(i for i in items if i.title == f.summary)
    print(f"{f.id}  {f.source:<6} {it.likelihood}x{it.impact}={it.likelihood * it.impact:>2} {f.severity:<6} due day {f.due_day}  "
          f"{f.owner:<14} {('compensating: ' + f.compensating) if f.compensating else ''}")
ch38 = {fid: sev for fid, _, sev, *_ in W.W38.RED_TEAM}
print(f"matches the security review's register (Chapter 38): {sum(ch38[f.id] == f.severity for f in new)} of {len(new)}")
plan = RemediationPlan(new)
print(f"open on day 127: {len(plan.open_on(127))}   due by pilot (day 131): {sum(f.due_day <= 131 for f in new)}")
