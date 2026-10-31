"""Figure 9.9: fifty answers from the model stand-in on the same three documents, against 73.0% and the 75% line."""
from _common import S, save, plt
import random, ltv_failure as L
rng = random.Random(2026); runs = [L.standin_model_ltv(rng) for _ in range(50)]
role = {"right": "system", "purchase price as value": "blocker", "prior charge left out": "data", "arithmetic slip": "cost"}
fig, ax = S.figure(3.9)
seen = {}; done = set()
for i, (shape, v) in enumerate(sorted(runs, key=lambda x: x[1])):
    seen[v] = seen.get(v, 0) + 1
    ax.scatter(v, seen[v], s=26, color=S.ROLE[role[shape]], zorder=3, label=None if shape in done else shape); done.add(shape)
ax.axvline(75, color=S.ROLE["blocker"], lw=S.LW["control"], ls="--"); ax.text(75.4, 25.5, "policy max 75%", fontsize=9.5)
ax.axvline(73, color=S.ROLE["system"], lw=S.LW["control"]); ax.text(72.6, 28.5, "correct 73.0%", fontsize=9.5, ha="right")
ax.set_xlabel("combined loan-to-value answered (%)"); ax.set_ylabel("runs"); ax.set_xlim(56, 88); ax.set_ylim(0, 31)
h, l = ax.get_legend_handles_labels(); ax.legend(h, l, fontsize=9, frameon=False, loc="upper left", bbox_to_anchor=(0.0, 0.82))
save(fig, 9)
