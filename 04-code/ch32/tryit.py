"""Try It Yourself. python tryit.py a | b | c"""
import sys
import _paths  # noqa: F401
from fieldkit.security import evidence_check, Threat, ThreatModel, AGENT
from world import ANSWERS, EVIDENCE, SCOPE, THREATS, findings

part = sys.argv[1] if len(sys.argv) > 1 else "a"
if part == "a":
    print("Try 1: rerun the evidence check on the day the pilot would start.")
    for day in (103, 131):
        v = evidence_check(ANSWERS, EVIDENCE, day, SCOPE)
        bad = [x for x in v if not x.passed and any("expired" in r for r in x.reasons)]
        print(f"  day {day}: {sum(x.passed for x in v)} of 41 pass; expired evidence under "
              + ", ".join(x.qid for x in bad))
elif part == "b":
    print("Try 2: add an email intake to the threat model and see what STRIDE alone would miss.")
    extra = [Threat("T23", "email intake", "spoofing", "lookalike clinic domain", 3, 3),
             Threat("T24", "email intake", AGENT, "instructions in the email body, not an attachment", 4, 4)]
    tm = ThreatModel(THREATS.system, THREATS.threats + extra)
    print(f"  threats {len(tm.threats)}; STRIDE alone {tm.stride_only()}; agent category {tm.by_category()[AGENT]}")
    print("  no control yet: " + ", ".join(t.id for t in tm.uncontrolled()))
elif part == "c":
    print("Try 3: push the high finding's date out without a compensating control.")
    f = [x for x in findings() if x.id == "F-09"][0]
    f.due_day, f.compensating = 160, ""
    print("  lint:", f.lint())
