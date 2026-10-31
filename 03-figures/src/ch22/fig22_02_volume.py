"""Figure 22.2: shadow-week documents by day and channel."""
import re
from _common import S, save, text
rows = re.findall(r"^(\d{3})\s+(\d+)\s+(\d+)\s+(\d+)$", text("breakdown"), re.M)
days = [r[0] for r in rows]
fig, ax = S.figure(height=4.0)
bottom = [0] * len(rows)
for j, (name, role) in enumerate([("EDI 210", "system"), ("scan", "data"), ("photo", "blocker")]):
    vals = [int(r[j + 1]) for r in rows]
    ax.bar(days, vals, bottom=bottom, color=S.ROLE[role], edgecolor=S.PAL["ink"], lw=S.LW["data"], label=name)
    bottom = [a + b for a, b in zip(bottom, vals)]
for x, t in zip(days, bottom):
    ax.text(x, t + 6, f"{t}", ha="center", fontsize=9, color=S.PAL["ink"])
ax.set_xlabel("engagement day (129 and 130 are a weekend)"); ax.set_ylabel("documents received")
ax.set_ylim(0, 430); ax.legend(loc="upper right", fontsize=9)
save(fig, 2, data="04-code/ch22/output/breakdown.txt")
