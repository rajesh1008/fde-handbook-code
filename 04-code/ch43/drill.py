"""Exit drill: Nadia Brooks runs MS-RB-01 (TMS feed late) at night as if Northlight were gone. Usage: python drill.py v0|v1
The 02:00 file is late; Pennant's deadline for matched results is 03:30. Stand-in minutes."""
import sys
import world as W
from fieldkit.handover import hhmm
from fieldkit.service import exit_drill


def run(v):
    rb = (W.RB_V0 if v == "v0" else W.RB_V1)[0]
    d = exit_drill(rb, W.OWNERS, "Nadia Brooks", W.DRILL_MINUTES, W.DRILL_WORKAROUND, start=120, deadline=210)
    print(f"EXIT DRILL  {rb.id} {rb.title}  runbooks {v}  by {d['person']}, Northlight hands off  (deterministic stand-in)")
    print("02:00  feed due; injected: file not delivered")
    for t, n, what in d["log"]:
        print(f"{hhmm(t)}  step {n}: {what}")
    if d["blocked_at"]:
        print(f"result: FAILED, blocked at step {d['blocked_at']}; deadline 03:30 missed")
    else:
        print(f"result: {'PASSED' if d['passed'] else 'FAILED'}, done {hhmm(d['end'])}, deadline 03:30, "
              f"{210 - d['end']} min to spare")
    return d


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "v0")
