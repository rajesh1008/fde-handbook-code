"""Figure 22.8: the shadow-week scorecard by channel, as scored by Pennant's reconciliation team."""
import re
from _common import S, save, text
rows = re.findall(r"^(edi|scan|photo|all)\s+(\d+)\s+([\d.]+)%\s+([\d.]+)%\s+([\d.]+)%\s+([\d.]+)%\s+(\d+)", text("scorecard"), re.M)
fig, ax = S.figure(height=4.2)
y = list(range(len(rows)))
left = [0.0] * len(rows)
for j, (name, role, hatch) in enumerate([("matched", "approval", None), ("exception", "evidence", "///"), ("held at door", "data", None), ("to a person", "model", None)]):
    vals = [float(r[j + 2]) for r in rows]
    ax.barh(y, vals, left=left, color=S.ROLE[role], edgecolor=S.PAL["ink"], lw=S.LW["data"], label=name, hatch=hatch)
    left = [a + b for a, b in zip(left, vals)]
for i, r in enumerate(rows):
    if int(r[6]):
        ax.text(101, i, f"{r[6]} wrong", va="center", fontsize=9, color=S.PAL["ink"])
ax.set_yticks(y); ax.set_yticklabels([f"{r[0]} ({r[1]})\n{r[2]}% matched" for r in rows]); ax.invert_yaxis()
ax.set_xlim(0, 112); ax.set_xlabel("share of documents (%)")
ax.legend(loc="lower left", fontsize=9, ncol=4, bbox_to_anchor=(0, -0.40))
save(fig, 8, data="04-code/ch22/output/scorecard.txt")
