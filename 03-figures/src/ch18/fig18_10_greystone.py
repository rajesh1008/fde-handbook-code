"""Figure 18.10: Greystone without embeddings: recall@5 of three lexical designs on the stand-in set."""
import re
from _common import S, save, text
fig, ax = S.figure(height=3.9)
rows = re.findall(r"^(lexical[^\n]*?)\s+recall@5 (\d+)/80 = ([\d.]+)$", text("greystone_capability"), re.M)
labels = [r[0].replace("lexical + ", "+ ").replace(" + synonym", "\n+ synonym") for r in rows]
vals = [float(r[2]) for r in rows]
ax.bar(range(len(vals)), vals, color=[S.ROLE["data"], S.ROLE["data"], S.ROLE["evidence"]], edgecolor=S.PAL["ink"], lw=S.LW["data"])
for i, (v, r) in enumerate(zip(vals, rows)):
    ax.text(i, v + 0.02, f"{v:.2f} ({r[1]}/80)", ha="center", fontsize=10)
ax.axhline(0.90, color=S.PAL["ink"], ls="--", lw=S.LW["control"]); ax.text(-0.4, 0.915, "agreed bar 0.90", fontsize=9)
ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels, fontsize=9); ax.set_ylim(0, 1.1); ax.set_ylabel("recall@5 (stand-in queries)")
save(fig, 10, data="04-code/ch18/output/greystone_capability.txt")
