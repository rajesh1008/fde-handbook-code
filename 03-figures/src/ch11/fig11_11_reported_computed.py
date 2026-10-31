"""Figure 11.11: reported versus computed status color, Greystone weeks 1 to 10."""
from _common import S, save
import status
rows = status.series()
mk = {"green": ("o", S.ROLE["approval"]), "amber": ("^", S.ROLE["data"]), "red": ("s", S.ROLE["blocker"])}
fig, ax = S.figure(3.7)
for w, d, rep, comp, fc in rows:
    for y, c in ((1, rep), (0, comp)):
        m, col = mk[c]; ax.scatter(w, y, marker=m, s=260, color=col, edgecolor=S.PAL["ink"], linewidth=0.75, zorder=3)
hidden = [w for w, d, rep, comp, fc in rows if rep != comp]
ax.axvspan(min(hidden) - 0.4, max(hidden) + 0.4, ymin=0.05, ymax=0.95, color=S.PAL["mist"], zorder=0)
ax.text((min(hidden) + max(hidden)) / 2, 1.55, f"{len(hidden)} weeks reported better than computed", ha="center", fontsize=9.5)
ax.set_yticks([0, 1]); ax.set_yticklabels(["computed", "reported"]); ax.set_ylim(-0.7, 1.9)
ax.set_xticks(range(1, 11)); ax.set_xlabel("week (circle green, triangle amber, square red)")
save(fig, 11)
