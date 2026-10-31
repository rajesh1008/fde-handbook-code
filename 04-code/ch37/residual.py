"""Residual risk in writing. Usage: residual.py v1|v2"""
import sys
import _paths  # noqa: F401
from fieldkit.gates import residual_lint
import world

v = sys.argv[1] if len(sys.argv) > 1 else "v2"
rs = world.residual(v)
print(f"RESIDUAL RISK  Caldwell Mutual  {'draft, day 156' if v == 'v1' else 'signed, day 157'}")
for r in rs:
    print(f"  {r.text:44} {r.accepted_by:16} day {r.day}  review {r.review_day}  control: {r.control or '-'}")
p = residual_lint(rs)
print(f"lint: {len(p)} problem(s)")
for x in p:
    print("  " + x)
