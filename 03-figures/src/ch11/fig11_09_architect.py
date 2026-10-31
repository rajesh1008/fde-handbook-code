"""Figure 11.9: days to a written answer from the Caldwell enterprise architect, by what was sent."""
from _common import S, save
import statistics, caldwell
fig, ax = S.figure(3.7)
roles = ["approval", "evidence", "blocker"]
for i, (k, days) in enumerate(caldwell.REVIEWS.items()):
    r = roles[i]
    for j, d in enumerate(sorted(days)):
        ax.scatter(d, i + (j - len(days) / 2) * 0.06, s=55, color=S.ROLE[r], edgecolor="white", zorder=3)
    med = statistics.median(days)
    ax.plot([med, med], [i - 0.3, i + 0.3], color=S.PAL["ink"], lw=S.LW["emphasis"])
    ax.text(med + 0.3, i - 0.32, f"median {med:g}", fontsize=9.5)
ax.set_yticks(range(3)); ax.set_yticklabels(list(caldwell.REVIEWS)); ax.invert_yaxis()
ax.set_xlim(0, 13.5); ax.set_ylim(2.6, -0.6); ax.set_xlabel("days to a written answer (n = 18 requests)")
save(fig, 9)
