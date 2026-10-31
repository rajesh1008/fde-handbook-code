"""Figure 9.6: the split of pipeline steps by class at the three customers."""
from _common import S, save, plt, CLASS_ROLE, CLASS_NAME, handles
from fieldkit.autonomy import split, CLASSES
import pipelines as pl
cust = [("Caldwell (12)", pl.CALDWELL), ("Greystone (25)", pl.GREYSTONE), ("Pennant (15, proposed)", pl.PENNANT)]
fig, ax = S.figure(3.8)
for i, (name, steps) in enumerate(cust):
    sp = split(steps); left = 0; n = len(steps)
    for k, r in zip(CLASSES, CLASS_ROLE):
        w = sp[k] / n
        ax.barh(i, w, left=left, height=0.55, color=S.ROLE[r], hatch=S.HATCH[r], edgecolor="white")
        if sp[k]: ax.text(left + w / 2, i, str(sp[k]), ha="center", va="center", fontsize=10, color=S.PAL["ink"], weight="bold",
                          bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
        left += w
ax.set_yticks(range(3)); ax.set_yticklabels([c for c, _ in cust], fontsize=9.5); ax.set_ylim(2.6, -1.3)
ax.set_xlim(0, 1); ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}")); ax.set_xlabel("share of steps")
ax.legend(handles(), CLASS_NAME, loc="upper center", ncol=4, fontsize=9, frameon=False, bbox_to_anchor=(0.45, 1.0))
save(fig, 6)
