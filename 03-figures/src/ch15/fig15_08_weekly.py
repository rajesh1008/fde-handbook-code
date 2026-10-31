"""Figure 15.8: something shipped every week before the data arrived, and most of it was reviewed by a named Caldwell person."""
import json
from _common import S, save, R
weeks = json.loads((R / "04-code/ch15/output/weekly_progress.json").read_text())
fig, ax = S.figure(height=3.8)
for w in weeks:
    x = w["week"]
    ax.bar(x - 0.2, w["shipped"], width=0.38, color=S.TINT["evidence"], hatch=S.HATCH["evidence"], edgecolor=S.ROLE["evidence"], lw=S.LW["data"])
    ax.bar(x + 0.2, w["reviewed"], width=0.38, color=S.ROLE["approval"], edgecolor=S.ROLE["approval"], lw=S.LW["data"])
ax.axvline(6.5, color=S.ROLE["data"], lw=S.LW["emphasis"])
S.label(ax, 6.45, 3.75, "real files, day 47", fs=9.5, ha="right")
ax.set_xticks([w["week"] for w in weeks]); ax.set_xlabel("week of the engagement"); ax.set_ylabel("items")
ax.set_ylim(0, 4.2); ax.set_yticks([0, 1, 2, 3])
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=S.TINT["evidence"], hatch=S.HATCH["evidence"], edgecolor=S.ROLE["evidence"], label="shipped"),
                   Patch(facecolor=S.ROLE["approval"], edgecolor=S.ROLE["approval"], label="reviewed by a named Caldwell person")],
          loc="upper left", frameon=True, edgecolor=S.PAL["light"], ncol=1)
save(fig, 8, data="04-code/ch15 weekly_progress.py")
