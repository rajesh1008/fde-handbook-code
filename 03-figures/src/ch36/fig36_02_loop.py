"""Figure 36.2: the joint red-team loop, from rules of engagement to a rerun that keeps the result valid."""
from _common import S, save, blank
fig, ax = S.figure(height=4.6); blank(ax, (0, 10), (0, 8))
steps = [("rules of\nengagement", "approval"), ("discovery\nhour", "evidence"), ("attack\ndays", "blocker"),
         ("report", "evidence"), ("joint\ntriage", "system"), ("fix and\nretest", "system"),
         ("residual\nrisk", "cost"), ("monthly\nrerun", "data")]
pos = [(0.2, 5.6), (2.7, 5.6), (5.2, 5.6), (7.7, 5.6), (7.7, 1.2), (5.2, 1.2), (2.7, 1.2), (0.2, 1.2)]
for (t, r), (x, y) in zip(steps, pos):
    S.box(ax, x, y, 2.1, 1.6, t, role=r, fs=10)
for i in range(3):
    S.arrow(ax, pos[i][0] + 2.1, 6.4, pos[i + 1][0], 6.4)
S.arrow(ax, 8.75, 5.6, 8.75, 2.8)
for i in range(4, 7):
    S.arrow(ax, pos[i][0], 2.0, pos[i + 1][0] + 2.1, 2.0)
S.arrow(ax, 1.25, 2.8, 1.25, 5.6, ls="--", color=S.PAL["grey"])
S.label(ax, 3.3, 4.2, "customer leads, FDE runs the desk", fs=9.5)
save(fig, 2, kind="diagram", data="Greystone days 121 to 131; Chapter 36 text")
