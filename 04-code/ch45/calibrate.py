"""Interviewer calibration on six recorded sessions. Usage: python calibrate.py before|after"""
import sys
import _paths  # noqa: F401
import world as W
from fieldkit.hiring import calibrate, exact_agreement

r = W.calibration(sys.argv[1])
cal = calibrate(r)
print(f"calibration {sys.argv[1]}: 6 sessions x 5 competencies x 3 interviewers")
for who, (off, exact, n) in cal.items():
    print(f"{who:<14} mean offset {off:+.2f}  equal to panel median {exact:.0%}  n {n}")
    for c in W.COMP:
        o = calibrate([x for x in r if x[2] == c])[who][0]
        if abs(o) >= 0.5:
            print(f"  DRIFT {who} on {c}: {o:+.2f}")
print(f"cells where all three agree exactly: {exact_agreement(r):.0%}")
