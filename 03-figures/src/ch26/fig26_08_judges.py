"""Figure 26.8: two judges measured against Anne's adjusters on the held-out split (Listing 26.4)."""
from _common import S, save, js
d = js("judge_validation")
fig, ax = S.figure(height=3.8)
names = [("judge_v1", "v1: Northlight rubric"), ("judge_v2", "v2: Caldwell rubric")]
for i, (k, lab) in enumerate(names):
    ax.bar(i * 3, d[k]["tpr"], color=S.ROLE["system"], hatch=S.HATCH["system"], edgecolor="white", width=0.9,
           label="TPR: passes what Anne passes" if i == 0 else None)
    ax.bar(i * 3 + 1, d[k]["tnr"], color=S.ROLE["blocker"], hatch=S.HATCH["blocker"], edgecolor="white", width=0.9,
           label="TNR: fails what Anne fails" if i == 0 else None)
    for x, v in ((i * 3, d[k]["tpr"]), (i * 3 + 1, d[k]["tnr"])):
        ax.text(x, v + 0.03, f"{v:.2f}", ha="center", fontsize=10)
ax.axhline(0.9, color=S.ROLE["system"], ls="--", lw=1); ax.axhline(0.8, color=S.ROLE["blocker"], ls="--", lw=1)
ax.set_xticks([0.5, 3.5], [n[1] for n in names])
ax.set_ylim(0, 1.15); ax.set_ylabel("rate on 2,010 fields")
ax.legend(loc="upper center", fontsize=9, ncol=1)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 8, data="04-code/ch26/output/judge_validation.json")
