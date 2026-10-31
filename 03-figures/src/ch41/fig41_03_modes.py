"""Figure 41.3: the runbook rule: failure class decides the mode; off returns through shadow."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4); blank(ax, (0, 10), (0, 7))
cls = [("quality", 5.4, "model"), ("data", 3.6, "data"), ("security", 1.8, "blocker"), ("availability", 0.1, "system")]
for t, y, r in cls:
    S.box(ax, 0.2, y, 2.4, 1.3, t, role=r, fs=10)
S.box(ax, 7.2, 5.4, 2.4, 1.3, "shadow", role="evidence", fs=10)
S.box(ax, 7.2, 2.7, 2.4, 1.3, "off", role="blocker", fs=10)
S.box(ax, 7.2, 0.1, 2.4, 1.3, "fail closed\nto manual queue", role="system", fs=9)
S.box(ax, 4.2, 5.4, 2.2, 1.3, "live", role="approval", fs=10)
S.arrow(ax, 2.6, 6.05, 4.2, 6.05); S.arrow(ax, 6.4, 6.05, 7.2, 6.05)
S.arrow(ax, 2.6, 4.25, 7.2, 3.5); S.arrow(ax, 2.6, 2.45, 7.2, 3.2); S.arrow(ax, 2.6, 0.75, 7.2, 0.75)
S.arrow(ax, 9.0, 4.0, 9.0, 5.4, ls="--", weight="emphasis")
S.label(ax, 7.4, 4.7, "returns via shadow", fs=9)
S.label(ax, 5.3, 4.95, "never off to live", fs=9)
save(fig, 3, kind="diagram", data="runbook rule (style sheet, Chapter 24); 04-code/ch41/world.py RUNBOOKS_V2; fieldkit/handover.py")
