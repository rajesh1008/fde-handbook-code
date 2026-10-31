"""Figure 12.9: what happened to the 32 claims in the submitted response by day 46 after signature (after_award.py)."""
from _common import S, plt, save, blank
fig, ax = S.figure(3.9); blank(ax, (0, 10), (0, 6))
S.box(ax, 0.1, 2.3, 2.0, 1.4, "response\n32 claims", role="evidence", fs=10)
S.box(ax, 3.0, 4.0, 2.4, 1.3, "stays as\nevidence 14", role="system", fs=10)
S.box(ax, 3.0, 0.7, 2.4, 1.3, "register 18", role="data", fs=10)
for y, t, r in ((3.0, "held 12", "approval"), (1.6, "renegotiated 2", "blocker"), (0.2, "decided 1, open 3", "data")):
    S.box(ax, 6.6, y, 3.2, 1.0, t, role=r, fs=10)
S.arrow(ax, 2.1, 3.3, 3.0, 4.6); S.arrow(ax, 2.1, 2.7, 3.0, 1.4)
for y in (3.5, 2.1, 0.7):
    S.arrow(ax, 5.4, 1.35, 6.6, y)
save(fig, 9, kind="diagram")
