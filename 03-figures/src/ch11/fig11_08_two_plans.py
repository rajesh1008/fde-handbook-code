"""Figure 11.8: two Greystone plans from the stand-in plan model: approvers at sign-off versus at design."""
from _common import S, save
import plan as P
a, pa = P.signoff_plan(); b, pb = P.design_plan()
role = {"build": "system", "security review": "blocker", "rework": "blocker", "re-review": "blocker",
        "security clinics": "approval", "final review": "approval", "buffer": "evidence"}
fig, ax = S.figure(3.8)
rows = [(f"sign-off: {p}", s, e, p) for p, s, e in a] + [(f"design: {p}", s, e, p) for p, s, e in b]
for i, (lab, s, e, p) in enumerate(rows):
    r = role[p]
    ax.barh(i, e - s, left=s, height=0.6, color=S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r])
for x, txt, y, ha, dx in ((pa, f"pilot day {pa}", 0, "left", 2), (pb, f"pilot day {pb}", 5, "right", -2)):
    ax.axvline(x, color=S.PAL["ink"], lw=S.LW["control"], ls="--"); ax.text(x + dx, y, txt, fontsize=9.5, va="center", ha=ha)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis()
ax.set_xlim(0, 215); ax.set_xlabel("engagement day (stand-in durations)")
save(fig, 8)
