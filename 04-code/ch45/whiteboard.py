"""Grade a whiteboard classification against the key. Usage: python whiteboard.py c214|c231"""
import sys
import _paths  # noqa: F401
import world as W
from fieldkit.hiring import classify_score

r = classify_score(W.CLASSIFY[sys.argv[1]], W.STEPS)
for step, want, got, mark in r["detail"]:
    print(f"{step:<30} key {want:<15} said {got:<15} {mark}")
print(f"agree {r['agree']} of {r['n']}, over-modeled {r['over']}, under {r['under']}, unsafe {r['unsafe']}")
