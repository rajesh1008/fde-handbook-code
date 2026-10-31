"""Figure 11.6: design changes found at Greystone days 3 to 19, by who surfaced them, sized by fix hours."""
from _common import S, save
import greystone as G
cats = ["coordinator", "security", "clinical", "operations"]
role = dict(coordinator="system", security="blocker", clinical="approval", operations="evidence")
fig, ax = S.figure(3.8)
for d, src, txt, h in G.DESIGN_CHANGES:
    y = cats.index(src)
    ax.scatter(d, y, s=40 + h * 35, color=S.TINT[role[src]], edgecolor=S.ROLE[role[src]], linewidth=1.5, hatch=S.HATCH[role[src]], zorder=3)
for c in cats:
    n = sum(1 for x in G.DESIGN_CHANGES if x[1] == c); hrs = sum(x[3] for x in G.DESIGN_CHANGES if x[1] == c)
    ax.text(20.3, cats.index(c), f"{n} change{'s' if n != 1 else ''}, {hrs} h", va="center", fontsize=9.5)
ax.axvspan(15, 19, color=S.PAL["mist"], zorder=0); ax.text(15.2, 3.55, "scoping week", fontsize=9.5)
ax.set_yticks(range(4)); ax.set_yticklabels(cats); ax.set_ylim(-0.6, 3.9); ax.set_xlim(2, 25)
ax.set_xticks([3, 5, 7, 9, 11, 13, 15, 17, 19]); ax.set_xlabel("engagement day the change was found (area: hours to fix at design)")
save(fig, 6)
