"""Figure 6.2: the day each path entered the log and the kind of source that put it there."""
from _common import S, plt, save, SHORT
from caldwell_discovery import build_log, PATHS
log = build_log()
mk = {"procedure": ("s", "evidence"), "interview": ("o", "model"), "shadow": ("D", "system"), "artifact": ("^", "data")}
fig, ax = S.figure(4.0)
for i, p in enumerate(PATHS):
    n = log.first_seen(p.pid)
    m, r = mk[n.source]
    ax.scatter([n.day], [i], marker=m, s=70, color=S.ROLE[r], zorder=3)
    ax.plot([8, n.day], [i, i], color=S.PAL["light"], lw=S.LW["data"], zorder=1)
ax.set_yticks(range(len(PATHS))); ax.set_yticklabels([SHORT[p.pid] for p in PATHS]); ax.invert_yaxis()
ax.set_xlim(7, 27); ax.set_xticks([8, 12, 16, 20, 24, 26]); ax.set_xlabel("engagement day")
for k, (m, r) in mk.items():
    ax.scatter([], [], marker=m, s=60, color=S.ROLE[r], label=k)
ax.legend(frameon=False, fontsize=9, loc="upper center", ncol=2, bbox_to_anchor=(0.7, 1.0))
save(fig, 2)
