"""Figure 11.5: what the two Greystone champions can do, and the two asks that belonged to an approver."""
from _common import S, save, blank
fig, ax = S.figure(4.0); blank(ax, ylim=(0, 6.2))
S.label(ax, 0.2, 5.75, "can be asked", fs=10, weight="bold")
S.label(ax, 7.0, 5.75, "cannot be asked", fs=10, weight="bold")
S.box(ax, 3.7, 3.6, 2.6, 0.9, "Monroe", role="data", fs=10)
S.box(ax, 3.7, 1.4, 2.6, 0.9, "Shah", role="data", fs=10)
for y, t in ((4.6, "introduce"), (3.5, "explain"), (2.4, "test drafts"), (1.3, "relay")):
    S.box(ax, 0.2, y - 0.35, 2.4, 0.7, t, role="system", fs=10)
for (y0, y1) in ((4.05, 4.6), (4.05, 3.5), (4.05, 2.4), (1.85, 3.5), (1.85, 1.3)):
    S.arrow(ax, 3.7, y0, 2.6, y1, weight="data")
S.box(ax, 7.0, 3.7, 2.8, 0.7, "approve: Hart", role="blocker", fs=10)
S.box(ax, 7.0, 1.5, 2.8, 0.7, "grant access: Oakley", role="blocker", fs=10)
S.arrow(ax, 6.3, 4.05, 7.0, 4.05, ls="--", color=S.ROLE["blocker"], weight="emphasis")
S.arrow(ax, 6.3, 1.85, 7.0, 1.85, ls="--", color=S.ROLE["blocker"], weight="emphasis")
S.label(ax, 7.0, 4.6, "asked day 12", fs=9.5); S.label(ax, 7.0, 2.4, "asked day 10", fs=9.5)
save(fig, 5, kind="diagram")
