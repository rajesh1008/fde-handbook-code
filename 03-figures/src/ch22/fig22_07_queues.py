"""Figure 22.7: where the documents that were not matched went, and who owns each queue."""
import re
from _common import S, save, text
rows = re.findall(r"^(sender request|clerk read|reconciliation|escalation)\s+(\d+)\s+(.+)$", text("routing"), re.M)
fig, ax = S.figure(height=4.0)
roles = ["data", "model", "evidence", "blocker"]
y = list(range(len(rows)))
ax.barh(y, [int(r[1]) for r in rows], color=[S.ROLE[x] for x in roles], edgecolor=S.PAL["ink"], lw=S.LW["data"])
for i, r in enumerate(rows):
    ax.text(int(r[1]) + 3, i, f"{r[1]}  {r[2]}", va="center", fontsize=9, color=S.PAL["ink"])
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis()
ax.set_xlim(0, 300); ax.set_xlabel("documents routed to people, days 124 to 130")
save(fig, 7, data="04-code/ch22/output/routing.txt")
