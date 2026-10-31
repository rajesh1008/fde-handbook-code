"""Pennant sprint 2: points by priority, ordering rule versus the plan as run."""
from _common import S, save, plt
from cadence_data import pennant_sprint2
from fieldkit.cadence import plan_sprint
roles = {"P0": "blocker", "P1": "approval", "P2": "system", "P3": "cost"}
names = {"P0": "P0 control", "P1": "P1 outcome", "P2": "P2 reuse", "P3": "P3 speed"}
plans = [("ordering rule", plan_sprint(pennant_sprint2(), 20)),
         ("as run (P-05 pinned)", plan_sprint(pennant_sprint2(), 20, pinned=("P-05", "P-03")))]
fig, ax = S.figure(3.9)
for y, (lab, p) in enumerate(plans):
    left = 0
    for pr in ("P0", "P1", "P2", "P3"):
        for i in [i for i in p.selected if i.priority == pr]:
            ax.barh(y, i.points, left=left, color=S.ROLE[roles[pr]], hatch=S.HATCH[roles[pr]], edgecolor="white", height=0.55)
            ax.text(left + i.points / 2, y, i.key, ha="center", va="center", fontsize=9,
                    color=S.PAL["ink"], bbox=dict(facecolor="white", edgecolor="none", pad=1))
            left += i.points
ax.axvline(20, color=S.PAL["ink"], lw=S.LW["control"], ls="--")
ax.text(20.2, 1.45, "capacity 20", fontsize=9)
ax.set_yticks([0, 1]); ax.set_yticklabels([p[0] for p in plans], fontsize=9)
ax.set_xlim(0, 24); ax.set_ylim(-0.6, 1.7); ax.set_xlabel("story points planned")
ax.text(0, -0.5, "  ".join(f"{names[k]}" for k in names), fontsize=9)
ax.invert_yaxis()
save(fig, 4)
