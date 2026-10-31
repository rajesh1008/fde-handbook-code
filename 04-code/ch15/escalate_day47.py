"""Chapter 15: the day-47 tracker, replayed from its history, reviewed by the escalation rules (fieldkit v2)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.histories import caldwell_history, caldwell_policy

tracker = caldwell_history().replay(47)
escalations, ours, quiet = caldwell_policy().review(tracker, today=47)
for e in escalations:
    print(e.note())
    print(f"rule:         {e.reason}\n")
for line in ours + quiet:
    print(line)
