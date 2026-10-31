"""Figure 19.6: read a mailbox as a queue: write durably, then acknowledge."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 12), (0, 6))
cols = [("mailbox", "data"), ("connector", "model"), ("document store", "system")]
for i, (t, r) in enumerate(cols):
    S.box(ax, 0.4 + i * 4.1, 4.7, 2.8, 0.9, t, role=r, fs=10)
    ax.plot([1.8 + i * 4.1] * 2, [0.4, 4.7], color=S.PAL["grey"], lw=0.75, ls="--")
S.arrow(ax, 1.8, 4.0, 5.9, 4.0); S.label(ax, 2.2, 4.15, "1 fetch", fs=9.5)
S.arrow(ax, 5.9, 3.0, 10.0, 3.0); S.label(ax, 6.3, 3.15, "2 dedupe, write", fs=9.5)
S.arrow(ax, 10.0, 2.2, 5.9, 2.2, ls="--", weight="data"); S.label(ax, 7.0, 1.8, "3 stored", fs=9.5)
S.arrow(ax, 5.9, 1.0, 1.8, 1.0, weight="emphasis"); S.label(ax, 2.3, 0.55, "4 acknowledge last", fs=9.5)
save(fig, 4, kind="diagram", data="fieldkit.connectors.MailQueue")
