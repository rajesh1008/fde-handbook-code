"""Check a take-home against an agent-only baseline. Usage: python takehome.py v0|v1"""
import sys
import _paths  # noqa: F401
import world as W
from fieldkit.hiring import takehome_validity

items = W.TAKEHOME[sys.argv[1]]
for n, w, a in items:
    print(f"{n:<42} weight {w:.2f}  {'agent-solvable' if a else 'needs the candidate'}")
r = takehome_validity(items)
print(f"agent-only baseline {r['agent_baseline']:.2f} against bar {r['bar']:.1f}; weight that needs the candidate {r['judgment_weight']:.2f}")
print("valid: the bar needs the candidate" if r["valid"] else "INVALID: an agent alone clears the bar")
