"""Figure 20.4: code lines shared by every estate against code lines specific to one."""
import re
from _common import S, save, text
rows = re.findall(r"^(core|adapter)\s+(\S+).*?(\d+) lines", text("loc"), re.M)
fig, ax = S.figure(height=3.9)
labels = [n.replace("fieldkit/", "") for _, n, _ in rows]
vals = [int(v) for _, _, v in rows]
cols = [S.ROLE["system"] if k == "core" else S.ROLE["model"] for k, _, _ in rows]
ax.barh(range(len(rows)), vals, color=cols, edgecolor=S.PAL["ink"], lw=S.LW["data"])
for i, v in enumerate(vals):
    ax.text(v + 3, i, str(v), va="center", fontsize=10)
ax.set_yticks(range(len(rows))); ax.set_yticklabels(labels); ax.invert_yaxis()
ax.set_xlim(0, 250); ax.set_xlabel("code lines (teal shared, navy per estate)")
save(fig, 4, data="04-code/ch20/output/loc.txt")
