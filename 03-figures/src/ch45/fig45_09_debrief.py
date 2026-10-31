"""Figure 45.9: three debriefs on loop v1. Medians per competency against the must-have bar and the floor."""
import re
from _common import S, save, text, COMPS
fig, ax = S.figure(height=4.4)
cand = (("c214", "blocker", "s", "214: no hire"), ("c236", "data", "D", "236: more evidence"), ("c231", "approval", "o", "231: hire"))
for k, (cid, role, m, lab) in enumerate(cand):
    t = text(f"debrief_{cid}")
    meds = [float(re.search(rf"{c}\s+scores \[[^\]]*\]\s+median\s+([\d.]+)", t).group(1)) for c in COMPS]
    ax.scatter([i + (k - 1) * 0.18 for i in range(5)], meds, marker=m, s=70, color=S.ROLE[role], label=lab, zorder=3)
ax.plot([-0.4, 0.4], [3, 3], color=S.PAL["ink"], lw=S.LW["emphasis"]); ax.plot([2.6, 3.4], [3, 3], color=S.PAL["ink"], lw=S.LW["emphasis"])
ax.axhline(2, color=S.ROLE["blocker"], ls="--", lw=S.LW["data"])
ax.text(4.45, 2.05, "floor 2", fontsize=9.5, ha="right", va="bottom"); ax.text(1.5, 3.55, "must-have bar 3\n(discovery, judgment)", fontsize=9.5, ha="center")
ax.set_xticks(range(5)); ax.set_xticklabels([c if c != "decomposition" else "decompo-\nsition" for c in COMPS])
ax.set_ylim(0.8, 4.4); ax.set_ylabel("median observed score (1 to 4)")
ax.legend(fontsize=9.5, loc="lower right"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 9, data="04-code/ch45/output/debrief_c214.txt, debrief_c231.txt, debrief_c236.txt")
