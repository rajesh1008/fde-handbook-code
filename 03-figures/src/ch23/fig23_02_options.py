"""Figure 23.2: yearly cost of the three store options including four re-embed events (store_options.txt)."""
import re
from _common import S, save, text
rows = re.findall(r"^([ABC]) (.+?)\s{2,}.*?\s([\d.]+)\s+([\d.]+)\s+(\w+)", text("store_options"), re.M)
fig, ax = S.figure(height=3.9)
col = {"refused": S.ROLE["blocker"], "deferred": S.PAL["grey"], "chosen": S.ROLE["approval"]}
for i, (k, name, m, y, st) in enumerate(rows):
    ax.barh(2 - i, float(y), color=col[st], height=0.55)
    ax.text(float(y) + 120, 2 - i, f"USD {float(y):,.0f}  {st}", va="center", fontsize=10, color=S.PAL["ink"])
ax.set_yticks([2, 1, 0], [f"{k}: {n.split(' on ')[0]}" for k, n, *_ in rows])
ax.set_xlim(0, 13500); ax.set_xlabel("USD a year, store plus four re-embeds (stand-in rates)")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 2, data="04-code/ch23/output/store_options.txt")
