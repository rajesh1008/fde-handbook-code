"""Figure 9.3: Caldwell's twelve steps in order, colored by class."""
from _common import S, save, plt, CLASS_ROLE, CLASS_NAME, handles
from fieldkit.autonomy import classify
import pipelines as pl
fig, ax = S.figure(3.67)
ax.set_xlim(-0.2, 12.2); ax.set_ylim(-1.5, 1.3); ax.axis("off")
tags = {"C02": "date", "C03": "policy", "C04": "lookup", "C06": "doc type", "C07": "loss code",
        "C09": "routing", "C11": "summary", "C12": "write"}
for i, s in enumerate(pl.CALDWELL):
    k = classify(s); r = CLASS_ROLE[k]
    ax.add_patch(plt.Rectangle((i + 0.05, -0.5), 0.9, 1.0, fc=S.ROLE[r], hatch=S.HATCH[r], ec="white", lw=1))
    ax.text(i + 0.5, 0, s.n[1:], ha="center", va="center", fontsize=10, color=S.PAL["ink"], weight="bold",
            bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"))
    if s.n in tags: ax.text(i + 0.5, -0.62 - 0.36 * (i % 2), tags[s.n], ha="center", va="top", fontsize=9)
ax.legend(handles(), CLASS_NAME, loc="upper center", ncol=4, fontsize=9, frameon=False, bbox_to_anchor=(0.5, 1.02))
save(fig, 3)
