"""Figure 33.2: the classification test as four ordered rules (Caldwell policy, day 80)."""
from _common import S, save, blank
fig, ax = S.figure(height=5.0); blank(ax, (0, 10), (0, 8))
qs = [(6.6, "quantitative method?"), (4.4, "trained or fitted on\nCaldwell data?"), (2.2, "feeds a core\ndecision?")]
for y, q in qs:
    S.box(ax, 0.3, y, 3.6, 1.2, q, role="model")
outs = [(6.6, "not a model:\nchange control", "system"), (4.4, "full scope\n(if core)", "approval"),
        (2.2, "registered,\nnot validated", "evidence")]
for y, t, r in outs:
    S.box(ax, 6.0, y, 3.7, 1.2, t, role=r)
S.box(ax, 6.0, 0.1, 3.7, 1.2, "registered\nas a tool", role="data")
S.arrow(ax, 3.9, 7.2, 6.0, 7.2); S.label(ax, 4.6, 7.35, "no", fs=9.5)
S.arrow(ax, 3.9, 5.0, 6.0, 5.0); S.label(ax, 4.6, 5.15, "yes", fs=9.5)
S.arrow(ax, 3.9, 2.8, 6.0, 2.8); S.label(ax, 4.6, 2.95, "yes", fs=9.5)
S.arrow(ax, 2.1, 6.6, 2.1, 5.6); S.label(ax, 2.25, 6.0, "yes", fs=9.5)
S.arrow(ax, 2.1, 4.4, 2.1, 3.4); S.label(ax, 2.25, 3.8, "no", fs=9.5)
S.arrow(ax, 2.1, 2.2, 2.1, 0.7); S.arrow(ax, 2.1, 0.7, 6.0, 0.7); S.label(ax, 2.25, 1.3, "no", fs=9.5)
save(fig, 2, kind="diagram", data="04-code/ch33/world.py (CALDWELL)")
