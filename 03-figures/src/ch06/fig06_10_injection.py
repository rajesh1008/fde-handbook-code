"""Figure 6.10: what the interviews alone report, and what one morning at the desk does to it."""
from _common import S, plt, save
steps = ["day 11\ninterviews", "day 12\nshadowed", "day 14\nresolved"]
naive = [3, 7, 7]; known = [3, 7, 7]; cov = [0, 3, 6]
fig, ax = S.figure(3.8)
x = range(3)
ax.bar([i - 0.2 for i in x], known, 0.38, color=S.TINT["data"], edgecolor=S.ROLE["data"], hatch="..", label="paths known")
ax.bar([i + 0.2 for i in x], cov, 0.38, color=S.ROLE["approval"], label="paths covered")
ax.plot([-0.4, 0.4], [3, 3], color=S.ROLE["blocker"], lw=S.LW["emphasis"])
ax.text(0, 3.3, "naive report: 3 of 3", ha="center", fontsize=9.5)
ax.text(1.2, 3.4, "P01 contradicted", ha="center", fontsize=9.5)
ax.set_xticks(list(x)); ax.set_xticklabels(steps); ax.set_ylim(0, 9); ax.set_ylabel("paths")
ax.legend(frameon=False, fontsize=9, loc="upper left")
save(fig, 10)
