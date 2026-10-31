"""RACI after hand-over. Usage: python raci.py v1|v2"""
import sys
import world as W
from fieldkit.handover import raci_check
rows = W.RACI_V1 if sys.argv[1] == "v1" else W.RACI_V2
f = dict(raci_check(rows, W.CW_PEOPLE))
for act, r, a, ci in rows:
    print(f"{act:<36}A: {a:<30}{('FAIL ' + f[act]) if act in f else 'ok'}")
print(f"activities: {len(rows)}   findings: {len(f)}")
