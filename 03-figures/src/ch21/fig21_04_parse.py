"""Figure 21.4: amounts read silently wrong by country with one parser for every layout; zero with the layout's locale."""
import re
from _common import S, save, text
t = text("variability")
rows = re.findall(r"^  ([A-Z]{2}):\s+(\d+) docs, silently wrong\s+(\d+)", t, re.M)
fig, ax = S.figure(height=3.9)
xs = range(len(rows))
ax.bar([x - 0.2 for x in xs], [int(r[1]) for r in rows], width=0.4, color=S.PAL["light"], edgecolor=S.PAL["grey"], label="documents")
ax.bar([x + 0.2 for x in xs], [int(r[2]) for r in rows], width=0.4, color=S.ROLE["blocker"], label="silently wrong, one parser")
ax.set_xticks(list(xs), [r[0] for r in rows]); ax.set_ylabel("documents")
ax.legend(loc="upper right", fontsize=10, frameon=True)
ax.text(3.6, 440, "with the layout's registered locale: 0 wrong", fontsize=10, color=S.PAL["ink"])
ax.set_ylim(0, 620); ax.spines[["top", "right"]].set_visible(False)
save(fig, 4, data="04-code/ch21/output/variability.txt")
