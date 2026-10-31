"""Figure 23.10: Caldwell's monthly retrieval cost by line at k=10, attributed to two cost centers (cost.txt)."""
import re
from _common import S, save, text
rows = re.findall(r"^(.{36}) Caldwell\s+(\S+)\S*.*?monthly\s+([\d.]+)", text("cost"), re.M)
fig, ax = S.figure(height=3.9)
rows = sorted(((n.strip(), cc, float(v)) for n, cc, v in rows), key=lambda r: r[2])
for i, (n, cc, v) in enumerate(rows):
    ax.barh(i, v, color=S.ROLE["cost"] if cc.startswith("CC-CLM") else S.ROLE["system"], height=0.55)
    ax.text(v + 0.6, i, f"USD {v:.2f}", va="center", fontsize=10, color=S.PAL["ink"])
ax.set_yticks(range(len(rows)), [r[0].replace(" in drafting calls", "").replace(" (pgvector)", "") for r in rows])
ax.set_xlim(0, 52); ax.set_xlabel("USD a month (stand-in rates); plum: claims, teal: platform")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 10, data="04-code/ch23/output/cost.txt")
