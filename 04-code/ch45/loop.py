"""Coverage matrix and lint for a loop. Usage: python loop.py v0|v1"""
import sys
import _paths  # noqa: F401
import world as W
from fieldkit.hiring import COMPETENCIES, lint_loop

lp = {"v0": W.LOOP_V0, "v1": W.LOOP_V1}[sys.argv[1]]
print(f"loop {lp.name}: {len(lp.rounds)} rounds")
print("round  " + "  ".join(f"{c[:6]:>6}" for c in COMPETENCIES) + "  minutes")
for r in lp.rounds:
    cells = []
    for c in COMPETENCIES:
        cells.append("   obs" if r.observes(c) else "  self" if r.asks(c) else "     .")
    print(f"{r.id:<6} " + "  ".join(cells) + f"  {r.minutes:>4}{' take-home' if r.takehome else ''}")
cov = lp.coverage()
print("observed in rounds: " + ", ".join(f"{c} {len(cov[c]['observed'])}" for c in COMPETENCIES))
top, share = lp.concentration()
live, home = lp.minutes()
print(f"most observed: {top} ({share:.0%} of observed probes); candidate time live {live} min, take-home {home} min")
f = lint_loop(lp)
for x in f:
    print(f"{x.code} {x.text}")
print(f"findings: {len(f)}")
