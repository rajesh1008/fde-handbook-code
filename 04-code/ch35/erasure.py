"""Chapter 35: trace one Pennant consignee through the map and show how each store lets them go.
Usage: erasure.py v1 | v2"""
import sys

import _paths  # noqa: F401
from fieldkit.privacy import erasure_trace, lint
from world import pennant

fixed = (sys.argv[1] if len(sys.argv) > 1 else "v1") == "v2"
hops = pennant(fixed)
trace = erasure_trace(hops, window=30)
print(f"Erasure trace, consignee contact on 14 EU shipments, Pennant map {'v2' if fixed else 'v1'}, window 30 days")
for name, how, days, ok in trace:
    print(f"  {name:<22} {how:<14} {'unknown' if days is None else f'{days:g} days':>9}  {'ok' if ok else 'FAILS'}")
bad = sum(not t[3] for t in trace)
worst = "none (a store cannot erase)" if bad else f"{max(d for _, _, d, _ok in trace):g} days"
print(f"stores holding the subject {len(trace)}   cannot erase {bad}   longest path to erasure {worst}")
found = lint(hops, {"GDPR"}, owner="Pennant")
print(f"GDPR lint findings {len(found)}")
for f in found:
    print(f)
