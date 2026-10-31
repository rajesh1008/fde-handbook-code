"""Figure 15.11: Greystone to day 112; whose move it was, day by day, on each request."""
from _common import S, save
from fieldkit.histories import greystone_history
h = greystone_history(); t = h.replay(112)
fig, ax = S.figure(height=3.9)
lanes = ["synthetic-referrals", "azure-subscription", "referral-sample"]
for i, k in enumerate(lanes):
    r = t.requests[k]; y = len(lanes) - 1 - i
    hist = r.ball_history + [(r.granted_day, "end")]
    for (d0, side), (d1, _) in zip(hist, hist[1:]):
        us = side == "us"
        ax.barh(y, d1 - d0, left=d0, height=0.5, color=S.TINT["cost"] if us else S.TINT["blocker"],
                hatch=S.HATCH["cost"] if us else S.HATCH["blocker"], edgecolor=S.ROLE["cost"] if us else S.ROLE["blocker"], lw=S.LW["data"])
    ax.plot([r.granted_day], [y], marker="D", color=S.ROLE["approval"], ms=7)
    ax.text(r.granted_day + 3, y, f"day {r.granted_day}", va="center", fontsize=9.5, color=S.PAL["ink"])
from matplotlib.patches import Rectangle
ax.add_patch(Rectangle((10, -0.25), 51, 0.5, fill=False, edgecolor=S.PAL["ink"], lw=S.LW["emphasis"], zorder=4))
ax.text(35.5, -0.62, "no owner, days 10 to 61", ha="center", va="center", fontsize=9.5, color=S.PAL["ink"])
ax.plot([40], [1.42], marker="x", color=S.ROLE["blocker"], ms=9, mew=2)
ax.text(41, 1.5, "day 40: email over Oakley's head", fontsize=9.5, color=S.PAL["ink"], va="bottom")
ax.plot([104], [-0.0], marker="x", color=S.ROLE["blocker"], ms=9, mew=2)
ax.text(103, 0.35, "key removed", fontsize=9.5, ha="right", color=S.PAL["ink"])
ax.set_yticks(range(len(lanes))); ax.set_yticklabels(list(reversed(lanes)), family="monospace", fontsize=9.5)
ax.set_xlim(0, 135); ax.set_ylim(-0.9, 2.7); ax.set_xlabel("engagement day")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=S.TINT["blocker"], hatch=S.HATCH["blocker"], edgecolor=S.ROLE["blocker"], label="Greystone's move"),
                   Patch(facecolor=S.TINT["cost"], hatch=S.HATCH["cost"], edgecolor=S.ROLE["cost"], label="our move")],
          loc="upper right", frameon=True, edgecolor=S.PAL["light"], ncol=2)
save(fig, 11, data="04-code/fieldkit histories.greystone_history()")
