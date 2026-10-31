"""Figure 14.7: the fax path found on day 19 doubles the step inventory and drops the deterministic share."""
from _common import S, save, plt, CLASS_ROLE
import pipeline as pl
from decision_tree import CLASSES, split, share

rows = [("electronic path\n(release 1)", pl.ELECTRONIC), ("fax path\n(found day 19)", pl.FAX),
        ("both paths", pl.ELECTRONIC + pl.FAX)]
names = ["deterministic", "rules + guardrails", "small model", "frontier + retrieval"]
fig, ax = S.figure(3.9)
for i, (n, steps) in enumerate(rows):
    sp = split(steps); left = 0
    for c, role in zip(CLASSES, CLASS_ROLE):
        v = sp[c]
        ax.barh(i, v, left=left, height=0.55, color=S.TINT[role], edgecolor=S.ROLE[role], hatch=S.HATCH[role], lw=1.2)
        ax.text(left + v / 2, i, str(v), ha="center", va="center", fontsize=9.5,
                bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
        left += v
    ax.text(left + 0.8, i, f"{len(steps)} steps, {share(steps):.0%} deterministic", va="center", fontsize=9.5)
ax.set_yticks(range(3)); ax.set_yticklabels([r[0] for r in rows], fontsize=9.5)
ax.set_ylim(2.6, -1.7); ax.set_xlim(0, 80); ax.set_xlabel("pipeline steps")
handles = [plt.Rectangle((0, 0), 1, 1, fc=S.TINT[r], ec=S.ROLE[r], hatch=S.HATCH[r]) for r in CLASS_ROLE]
ax.legend(handles, names, loc="upper right", ncol=2, fontsize=9, frameon=False)
save(fig, 7)
