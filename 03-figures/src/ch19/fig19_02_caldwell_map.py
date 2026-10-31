"""Figure 19.2: Caldwell's intake and claims-core surfaces as wired on the sample."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4)
blank(ax, (0, 12), (0, 7.2))
for i, t in enumerate(["mailbox", "scan drop", "fax folder"]):
    S.box(ax, 0.2, 5.4 - i * 1.6, 2.4, 1.1, t, role="data", fs=10)
    S.arrow(ax, 2.6, 5.95 - i * 1.6, 4.0, 4.4 - (i - 1) * 0.4, weight="data")
S.box(ax, 4.0, 2.9, 3.2, 2.2, "overlay\nconnectors,\nmodel, outbox", role="model", fs=10.5)
S.box(ax, 8.8, 4.6, 3.0, 1.6, "claims-core\n(2009)", role="system", fs=10.5)
S.box(ax, 8.8, 1.2, 3.0, 1.3, "adjuster queue", role="approval", fs=10)
S.arrow(ax, 7.2, 4.6, 8.8, 5.2); S.label(ax, 7.3, 5.4, "screens", fs=9.5)
S.arrow(ax, 9.6, 4.6, 6.6, 5.1, ls="--", weight="data"); S.label(ax, 8.0, 3.7, "extract", fs=9.5)
S.arrow(ax, 7.2, 3.2, 8.8, 1.9); S.label(ax, 7.0, 1.6, "held", fs=9.5)
S.label(ax, 0.2, 0.4, "zero changes inside claims-core", fs=10, color=S.PAL["slate"])
save(fig, 2, kind="diagram", data="04-code/ch19/reconcile_caldwell.py")
