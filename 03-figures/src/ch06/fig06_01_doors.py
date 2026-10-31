"""Figure 6.1: the three doors in the 2014 procedure against the eleven found by day 26."""
from _common import S, plt, save, blank, SHORT
from caldwell_discovery import PATHS
fig, ax = S.figure(4.6); blank(ax, (0, 10), (0, 12.4))
S.label(ax, 1.6, 11.9, "2014 procedure", ha="center", fs=10, weight="bold")
S.label(ax, 6.9, 11.9, "watched by day 26", ha="center", fs=10, weight="bold")
for i, p in enumerate(PATHS[:3]):
    S.box(ax, 0.3, 10.2 - i * 1.05, 2.6, 0.8, SHORT[p.pid], role="system", fs=9.5)
for i, p in enumerate(PATHS):
    col, row = divmod(i, 6)
    x = 4.2 + col * 2.9; y = 10.2 - row * 1.05
    S.box(ax, x, y, 2.6, 0.8, SHORT[p.pid], role="system" if p.documented else "data", fs=9.5)
for i in range(3):
    S.arrow(ax, 2.95, 10.6 - i * 1.05, 4.15, 10.6 - i * 1.05, weight="data")
S.label(ax, 4.2, 3.1, "teal, hatched: in the procedure", fs=9.5)
S.label(ax, 4.2, 2.4, "amber, dotted: found by watching", fs=9.5)
save(fig, 1, kind="diagram")
