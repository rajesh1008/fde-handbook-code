"""Figure 15.1: Caldwell Mutual's access requests to day 47, grouped by ladder rung (data from fieldkit fixtures)."""
import sys, pathlib
R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "05-build/design")); sys.path.insert(0, str(R / "04-code/fieldkit"))
import fde_style as S
import matplotlib.pyplot as plt
from fieldkit import LADDER
from fieldkit.fixtures import caldwell_tracker

S.apply()
TODAY = 47
t = caldwell_tracker()
order = {k: i for i, k in enumerate(LADDER)}
reqs = sorted(t.requests.values(), key=lambda r: (order[r.rung], r.requested_day or 999))
fig, ax = plt.subplots(figsize=(8, 4.8))
for i, r in enumerate(reqs):
    y = len(reqs) - 1 - i
    if r.requested_day is None:
        ax.text(TODAY + 1, y, "not yet requested", va="center", fontsize=8.5, color=S.PAL["slate"], style="italic")
    else:
        end = r.granted_day if r.status == "granted" else TODAY
        role = "approval" if r.status == "granted" else "blocker"
        ax.barh(y, max(end - r.requested_day, 0.6), left=r.requested_day, height=0.55,
                color=S.ROLE[role], alpha=0.85 if role == "approval" else 0.9,
                hatch="" if role == "approval" else "//", edgecolor="white")
        lab = f"{end - r.requested_day} d" + ("" if r.status == "granted" else f"  open: {r.owner}")
        ax.text(end + 0.8, y, lab, va="center", fontsize=8.5, color=S.PAL["ink"])
ax.set_yticks(range(len(reqs)))
ax.set_yticklabels([f"{r.key}  ({r.rung})" for r in reversed(reqs)], fontsize=8.5)
ax.axvline(TODAY, color=S.ROLE["data"], lw=2)
ax.set_ylim(-0.8, len(reqs) - 0.4)
ax.text(TODAY - 0.8, 0, "day 47: 200 real files arrive", ha="right", va="center", fontsize=8.5, color=S.PAL["ink"])
ax.set_xlim(0, 78); ax.set_xlabel("engagement day")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=S.ROLE["approval"], label="granted"),
                   Patch(facecolor=S.ROLE["blocker"], hatch="//", edgecolor="white", label="waiting")],
          loc="upper right", frameon=False, fontsize=9)
ax.set_title("Ladder position on day 47: synthetic (1 of 4)", loc="left", fontsize=11, color=S.PAL["ink"], pad=10)
fig.savefig(pathlib.Path(__file__).with_name("fig15-01.png"), dpi=200)
