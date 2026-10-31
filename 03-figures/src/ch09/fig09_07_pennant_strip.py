"""Figure 9.7: Pennant's fifteen proposed steps in order, colored by class."""
from _common import S, save, plt, CLASS_ROLE, CLASS_NAME, handles
from fieldkit.autonomy import classify
import pipelines as pl
fig, ax = S.figure(3.67)
n = len(pl.PENNANT); ax.set_xlim(-0.2, n + 0.2); ax.set_ylim(-1.6, 1.6); ax.axis("off")
tags = {"N03": "layout", "N05": "handwritten", "N12": "email draft"}
for i, s in enumerate(pl.PENNANT):
    r = CLASS_ROLE[classify(s)]
    ax.add_patch(plt.Rectangle((i + 0.05, -0.5), 0.9, 1.0, fc=S.ROLE[r], hatch=S.HATCH[r], ec="white"))
    ax.text(i + 0.5, 0, s.n[1:], ha="center", va="center", fontsize=9, color=S.PAL["ink"], weight="bold",
            bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
    if s.n in tags: ax.text(i + 0.5, -0.72, tags[s.n], ha="center", va="top", fontsize=9)
ax.legend(handles(), CLASS_NAME, loc="upper center", ncol=4, fontsize=9, frameon=False, bbox_to_anchor=(0.5, 1.02))
save(fig, 7)
