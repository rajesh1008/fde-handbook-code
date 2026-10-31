"""Figure 16.13: the shadow tap: live documents pass through, only agreement and a profile are kept."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6))
S.box(ax, 0.1, 3.6, 2.2, 1.3, "live document", role="data", fs=10)
S.box(ax, 3.0, 3.6, 2.2, 1.3, "extractor", role="model", fs=10.5)
S.box(ax, 3.0, 1.0, 2.2, 1.3, "adjuster's\nkeyed record", role="approval", fs=10)
S.box(ax, 6.2, 2.3, 3.6, 1.3, "kept: keyed id,\nagreement, profile", role="evidence", fs=10)
S.box(ax, 6.2, 4.4, 3.6, 1.1, "not kept: text, values", role="cost", fs=10, ls="--")
S.arrow(ax, 2.3, 4.25, 3.0, 4.25); S.arrow(ax, 5.2, 4.0, 6.2, 3.2); S.arrow(ax, 5.2, 1.65, 6.2, 2.7)
S.label(ax, 6.2, 1.3, "canary scan proves it", fs=10, color=S.PAL["slate"])
save(fig, 13, kind="diagram", data="04-code/fieldkit/fieldkit/shadow.py")
