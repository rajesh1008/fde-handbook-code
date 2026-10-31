"""Figure 5.6: the two new hires' first-month disagreements by axis, and whose instinct the ruling kept."""
from _common import S, save, plt, FIGSIZE
from disagreements import AXES, LOG

cats = [("C", "Callum (integrator)", "system"), ("S", "Sofia (lab)", "model"),
        ("both", "both", "data"), ("neither", "neither: vendor rule", "evidence")]
fig, ax = plt.subplots(figsize=FIGSIZE)
left = [0] * len(AXES)
for key, lab, role in cats:
    vals = [sum(1 for e in LOG if e[1] == a and e[6] == key) for a in AXES]
    ax.barh(range(len(AXES)), vals, left=left, color=S.ROLE[role], hatch=S.HATCH[role],
            edgecolor="white", height=0.6, label=lab)
    left = [l + v for l, v in zip(left, vals)]
ax.set_yticks(range(len(AXES))); ax.set_yticklabels(AXES, fontsize=9.5); ax.invert_yaxis()
ax.set_xlim(0, 4.6); ax.set_xticks(range(5)); ax.set_xlabel("disagreements logged, days 1 to 30")
ax.legend(loc="lower right", fontsize=9, frameon=True, fancybox=False)
save(fig, 8)
