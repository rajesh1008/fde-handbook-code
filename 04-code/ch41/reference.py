"""Engagement reference reading paths. Usage: python reference.py v1|v2"""
import sys
import world as W
from fieldkit.handover import path_coverage
paths = W.PATHS_V1 if sys.argv[1] == "v1" else W.PATHS_V2
gaps = path_coverage(paths, W.NEEDS)
total = sum(m for _, m in W.SECTIONS.values())
print(f"engagement reference: {len(W.SECTIONS)} sections, {total} minutes end to end")
for s, secs in paths.items():
    mins = sum(W.SECTIONS[x][1] for x in secs)
    g = gaps.get(s, [])
    print(f"{s:<18}sections {','.join(map(str, secs)):<16}{mins:>3} min  "
          + ("ok" if not g else "missing " + ", ".join(f"{x} {W.SECTIONS[x][0]}" for x in g)))
print(f"paths with gaps: {len(gaps)} of {len(paths)}")
