"""Figure 45.2: loop v1 coverage. Every competency observed in at least two rounds; no round probes more than two."""
from _common import S, save, coverage, heat
rows = coverage("loop_v1")
assert len(rows) == 6
fig, ax = S.figure(height=4.4)
heat(ax, rows)
for s in ax.spines.values():
    s.set_visible(False)
save(fig, 2, data="04-code/ch45/output/loop_v1.txt")
