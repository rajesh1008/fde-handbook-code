"""Figure 9.14: outcomes by step on 400 synthetic documents: correct, caught loudly, wrong silently."""
from _common import S, save, plt
import accuracy_run as A
rows = A.score(); names = list(rows)
fig, ax = S.figure(4.0)
for i, n in enumerate(names):
    r = rows[n]; left = 0
    for key, role in (("correct", "system"), ("caught", "data"), ("silent", "blocker")):
        ax.barh(i, r[key], left=left, height=0.55, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white",
                label=key if i == 0 else None)
        left += r[key]
    ax.text(404, i, f"{r['caught']} caught, {r['silent']} silent", va="center", fontsize=9)
ax.set_yticks(range(len(names))); ax.set_yticklabels(names, fontsize=9)
ax.set_xlim(300, 520); ax.set_xticks([300, 350, 400]); ax.set_xlabel("documents (axis starts at 300)")
ax.set_ylim(len(names) - 0.4, -1.4)
ax.legend(fontsize=9, frameon=False, loc="upper left", ncol=3)
save(fig, 14)
