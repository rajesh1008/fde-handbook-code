"""Figure 24.11: token brokerage. One assertion for the brain crosses; the broker exchanges it per source on behalf
of the user (identity.txt, split.txt)."""
import re
from _common import S, save, blank, text
assert "600/600 turns refused" in text("identity")
fig, ax = S.figure(height=4.4)
blank(ax, (0, 10), (0, 6))
S.box(ax, 0.2, 4.2, 2.2, 1.0, "suite sign-in", role="approval", fs=10)
S.box(ax, 0.2, 2.2, 2.2, 1.0, "surface", role="system", fs=10)
S.arrow(ax, 1.3, 4.2, 1.3, 3.2)
S.label(ax, 1.4, 3.6, "aud nl-brain", fs=10, family="monospace")
S.box(ax, 3.6, 2.2, 2.2, 1.0, "token broker", role="approval", fs=10)
S.arrow(ax, 2.4, 2.7, 3.6, 2.7, weight="emphasis")
ax.axvline(3.0, color=S.PAL["ink"], lw=S.LW["emphasis"], ls=(0, (2, 3)), ymin=0.05, ymax=0.95)
for i, s in enumerate(["policy", "claims", "retrieval", "loss history", "rules", "documents"]):
    y = 5.0 - i * 0.85
    S.box(ax, 7.4, y, 2.4, 0.62, s, role="data", fs=10)
    S.arrow(ax, 5.8, 2.7, 7.4, y + 0.31, weight="data")
S.label(ax, 6.0, 0.35, "on behalf of the adjuster, 15 min", fs=10)
S.box(ax, 0.2, 0.2, 2.6, 1.2, "suite token\nforwarded: refused", role="blocker", fs=10, ls="--")
save(fig, 11, kind="diagram", data="04-code/ch24/output/identity.txt")
