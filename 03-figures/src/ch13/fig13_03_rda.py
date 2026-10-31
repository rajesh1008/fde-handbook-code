"""Ready, Done, Accepted: the three gates on one item and the three outcomes of acceptance."""
from _common import S, save, blank
fig, ax = blank(3.9)
S.box(ax, 1, 40, 18, 22, "Ready\nowner,\ntestable", role="evidence", fs=9)
S.box(ax, 27, 40, 18, 22, "Done\nevidence\nattached", role="system", fs=9)
S.arrow(ax, 19, 51, 27, 51); S.arrow(ax, 45, 51, 55, 51)
S.box(ax, 55, 70, 42, 18, "accepted", role="approval", fs=10)
S.box(ax, 55, 42, 42, 18, "accepted, dated\nfollow-up", role="data", fs=10)
S.box(ax, 55, 14, 42, 18, "not accepted:\ncarried over", role="blocker", fs=10)
S.arrow(ax, 50, 51, 55, 79); S.arrow(ax, 50, 51, 55, 23)
save(fig, 3, kind="diagram")
