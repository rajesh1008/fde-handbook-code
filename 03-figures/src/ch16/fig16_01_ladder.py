"""Figure 16.1: the four rungs of the data access ladder and the one claim each rung supports."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6))
rungs = [("synthetic", "the plumbing\nruns", "data"), ("sampled", "accuracy on a\nsigned sample", "evidence"),
         ("shadowed", "agreement on\nlive traffic", "system"), ("live", "outcomes", "approval")]
for i, (r, claim, role) in enumerate(rungs):
    x, y = 0.1 + i * 2.5, 0.8 + i * 0.9
    S.box(ax, x, y, 2.0, 1.0, r, role=role, fs=11)
    S.label(ax, x + 1.0, y + 1.15, claim, fs=10, ha="center", va="bottom")
    if i < 3:
        S.arrow(ax, x + 2.0, y + 0.5, x + 2.5, y + 1.4)
S.label(ax, 0.1, 0.2, "each rung licenses one more kind of claim", fs=10, color=S.PAL["slate"])
save(fig, 1, kind="diagram", data="chapter text (access ladder, Chapter 15)")
