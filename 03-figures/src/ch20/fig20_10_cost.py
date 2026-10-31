"""Figure 20.10: cost per scored document on each estate, model calls and fixed estate costs."""
import re
from _common import S, save, text
rows = re.findall(r"^(\w+) \(([^)]+)\)\s+model ([\d.]+)\s+fixed ([\d.]+)\s+total ([\d.]+)", text("cost_estate"), re.M)
fig, ax = S.figure(height=3.9)
labels = [f"{a}\n{b}" for a, b, *_ in rows]
m = [float(r[2]) for r in rows]; f = [float(r[3]) for r in rows]
ax.bar(range(3), m, color=S.ROLE["model"], edgecolor=S.PAL["ink"], lw=S.LW["data"], label="model calls")
ax.bar(range(3), f, bottom=m, color=S.ROLE["cost"], edgecolor=S.PAL["ink"], lw=S.LW["data"], label="fixed, spread over volume")
for i, r in enumerate(rows):
    ax.text(i, float(r[4]) + 0.006, f"USD {float(r[4]):.3f}", ha="center", fontsize=10)
ax.set_xticks(range(3)); ax.set_xticklabels(labels); ax.set_ylabel("USD per scored document"); ax.set_ylim(0, 0.31)
ax.legend(loc="upper right", fontsize=9)
save(fig, 10, data="04-code/ch20/output/cost_estate.txt (stand-in rates and volumes)")
