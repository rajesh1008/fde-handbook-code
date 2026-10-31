"""Figure 45.1: loop v0 coverage. Build is observed in three of five rounds; three competencies are never observed."""
from _common import S, save, coverage, heat
rows = coverage("loop_v0")
assert [r[0] for r in rows] == ["R1", "R2", "R3", "R4", "R5"]
fig, ax = S.figure(height=4.2)
heat(ax, rows)
for s in ax.spines.values():
    s.set_visible(False)
save(fig, 1, data="04-code/ch45/output/loop_v0.txt")
