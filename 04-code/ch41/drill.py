"""The hand-over drill: the customer team runs a failure drill alone. Usage: python drill.py 1|2|pennant|pennant-rerouted"""
import sys
import world as W
from fieldkit.handover import drill, hhmm
m = sys.argv[1]
if m in ("1", "2"):
    alerts = W.ALERTS_V1 if m == "1" else W.ALERTS_V2
    r = drill(W.KEY_DRILL, alerts, W.ROTA, W.RB03_MINUTES, W.CW)
    print(f"Caldwell drill {m} (day {176 if m == '1' else 183}): {W.KEY_DRILL.name}; Northlight observes, hands off")
    print("02:00 key rotates; adapter keeps the old key; 03:00 grace ends, gateway returns 401")
else:
    alerts = W.PN_ALERTS_V1 if m == "pennant" else W.PN_ALERTS_V2
    r = drill(W.PN_DRILL, alerts, W.PN_ROTA, W.PN_MINUTES, W.PN)
    print(f"Pennant drill ({'as built' if m == 'pennant' else 'alerts rerouted to Pennant'}): {W.PN_DRILL.name}; deadline 03:30 Central")
    print("02:00 TMS CSV lands; 02:04 volume guard holds the file")
for t, e in r["log"]:
    print(f"{hhmm(t)}  {e}")
det = "never (no customer acknowledgment)" if r["detect"] is None else f"{r['detect']} min"
mit = "never" if r["mitigate"] is None else f"{r['mitigate']} min"
print(f"time to detect {det}; time to mitigate {mit}; vendor touches {r['touches']}"
      + ("; deadline missed" if r["deadline_missed"] else ""))
print("drill " + ("PASSED" if r["passed"] else "FAILED") + " (criteria: detect <= 15 min, mitigate <= 60 min, no vendor touch)")
