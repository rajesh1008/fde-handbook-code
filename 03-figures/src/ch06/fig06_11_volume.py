"""Figure 6.11: monthly volume by path; the found paths carry 37 percent."""
from _common import S, plt, save, SHORT
from caldwell_discovery import PATHS
fig, ax = S.figure(4.2)
ps = sorted(PATHS, key=lambda p: p.volume)
for i, p in enumerate(ps):
    r = "system" if p.documented else "data"
    ax.barh(i, p.volume, color=S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r], lw=S.LW["data"])
    ax.text(p.volume + 60, i, f"{p.volume:,}", va="center", fontsize=9)
ax.set_yticks(range(len(ps))); ax.set_yticklabels([SHORT[p.pid] for p in ps])
ax.set_xlabel("documents a month (Caldwell's own counts)"); ax.set_xlim(0, 4900)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=S.TINT["system"], edgecolor=S.ROLE["system"], hatch="//", label="in the procedure"),
                   Patch(facecolor=S.TINT["data"], edgecolor=S.ROLE["data"], hatch="..", label="found")],
          frameon=False, fontsize=9, loc="lower right")
save(fig, 11)
