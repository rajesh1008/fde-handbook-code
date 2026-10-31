"""Figure 22.5: the fifteen steps as built, by how many documents ran each one in the shadow week."""
import re
from _common import S, save, text
rows = re.findall(r"^(N\d\d)\s+(det|rules|small|frontier)\s+(\d+)", text("steps"), re.M)
role = {"det": "system", "rules": "evidence", "small": "model", "frontier": "cost"}
name = {"det": "deterministic", "rules": "written rules", "small": "small model", "frontier": "frontier model"}
fig, ax = S.figure(height=5.2)
y = list(range(len(rows)))
seen = set()
for i, (n, c, runs) in enumerate(rows):
    ax.barh(i, int(runs), color=S.ROLE[role[c]], edgecolor=S.PAL["ink"], lw=S.LW["data"], label=None if c in seen else name[c])
    seen.add(c)
    ax.text(int(runs) + 20, i, "off in shadow" if int(runs) == 0 else f"{int(runs):,}", va="center", fontsize=9, color=S.PAL["ink"])
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis()
ax.set_xlim(0, 2500); ax.set_xlabel("documents that ran the step, days 124 to 130")
ax.legend(loc="lower right", fontsize=9)
save(fig, 5, data="04-code/ch22/output/steps.txt")
