"""Runbook lint. Usage: python runbooks.py v1|v2"""
import sys
import world as W
from fieldkit.handover import lint_runbook
rbs, alerts = (W.RUNBOOKS_V1, W.ALERTS_V1) if sys.argv[1] == "v1" else (W.RUNBOOKS_V2, W.ALERTS_V2)
total = 0
for rb in rbs:
    f = lint_runbook(rb, W.CW_PEOPLE, alerts)
    total += len(f)
    print(f"{rb.id} {rb.title:<34} {rb.failure_class:<13}{rb.mode:<12}owner {rb.owner:<16}{len(rb.steps)} steps  "
          + ("ok" if not f else f"{len(f)} finding" + ("s" if len(f) > 1 else "")))
    for rule, d in f:
        print(f"    {rule}  {d}")
print(f"runbooks: {len(rbs)}   findings: {total}")
