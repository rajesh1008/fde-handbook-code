"""Figure 28.3: the life of one rule."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4); blank(ax, (0, 10), (0, 7))
steps = [(0.2, 5.2, "heard or read", "model"), (3.6, 5.2, "rule card", "evidence"), (7.0, 5.2, "check + two tests", "system"),
         (7.0, 2.8, "VERIFY: runs strict", "data"), (3.6, 2.8, "owner signs", "approval"), (0.2, 2.8, "in the suite", "system"),
         (0.2, 0.4, "retired, kept", "evidence")]
for x, y, lab, r in steps:
    S.box(ax, x, y, 2.8, 1.1, lab, role=r)
S.arrow(ax, 3.0, 5.75, 3.6, 5.75); S.arrow(ax, 6.4, 5.75, 7.0, 5.75); S.arrow(ax, 8.4, 5.2, 8.4, 3.9)
S.arrow(ax, 7.0, 3.35, 6.4, 3.35); S.arrow(ax, 3.6, 3.35, 3.0, 3.35); S.arrow(ax, 1.6, 2.8, 1.6, 1.5)
S.arrow(ax, 3.0, 3.1, 7.0, 6.0, ls="--", weight="data")
S.label(ax, 5.4, 4.5, "changed", fs=9)
save(fig, 3, kind="diagram", data="04-code/ch28/rules.py")
