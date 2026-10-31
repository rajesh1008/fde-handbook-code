"""Figure 47.7: two features from the field on the function's month clock: waiting before triage, building after."""
from _common import S, save
import sys
sys.path.insert(0, str(S.ROOT / "04-code/ch47"))
from world import SHIPPED  # noqa: E402
fig, ax = S.figure(height=3.8)
for y, s in enumerate(SHIPPED[::-1]):
    ax.barh(y, s["triaged_month"] - s["first_month"], 0.45, left=s["first_month"], color=S.ROLE["blocker"],
            hatch="\\\\", ec="white")
    ax.barh(y, s["shipped_month"] - s["triaged_month"], 0.45, left=s["triaged_month"], color=S.ROLE["approval"],
            ec="white")
    ax.text(s["shipped_month"] + 0.2, y, f"{len(s['adopted'])} engagements", va="center", fontsize=9)
ax.set_yticks([0, 1]); ax.set_yticklabels(["quality gate (Pennant)", "key refresh (Caldwell)"])
ax.axvline(13, color=S.PAL["ink"], ls="--", lw=0.75); ax.text(13.1, 1.4, "loop starts", fontsize=9)
ax.set_xlim(0, 21); ax.set_ylim(-1.4, 1.7); ax.set_xlabel("function month")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc=S.ROLE["blocker"], hatch="\\\\", ec="white", label="reported, no triage"),
                   Patch(fc=S.ROLE["approval"], label="triaged to shipped")], loc="lower center", ncol=2, fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 7, data="04-code/ch47/output/loop_ship.txt; world.py SHIPPED")
