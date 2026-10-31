"""Alert routing check: every alert lands at a destination the customer owns. Usage: python routes.py v1|v2|pennant"""
import sys
import world as W
from fieldkit.handover import route_check
alerts, dom = {"v1": (W.ALERTS_V1, W.CW), "v2": (W.ALERTS_V2, W.CW), "pennant": (W.PN_ALERTS_V1, W.PN)}[sys.argv[1]]
bad = route_check(alerts, dom)
print(f"alert rules: {len(alerts)}   customer domains: {', '.join(sorted(dom))}")
for a in alerts:
    print(f"{a.id:<6}{a.monitor:<36}{a.dest:<42}{'VENDOR' if a in bad else 'ok'}")
print(f"routed outside the customer: {len(bad)}" + (f" ({', '.join(a.id for a in bad)})" if bad else ""))
