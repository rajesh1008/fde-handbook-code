"""Figure 32.8: the review result by theme: passed and findings."""
import re
from collections import Counter
from _common import S, save, text, world
rows = re.findall(r"^([a-z ]+?)\s{2,}(\d+)\s+(\d+)\s{2}", text("triage"), re.M)
theme = {a.qid: a.theme for a in world.ANSWERS}
fnd = Counter(theme[f.source] for f in world.findings())
fig, ax = S.figure(height=4.2)
for i, (t, n, _) in enumerate(rows):
    f = fnd[t]; p = int(n) - f
    ax.barh(i, p, color=S.TINT["approval"], edgecolor=S.ROLE["approval"], label="passed" if i == 0 else None)
    ax.barh(i, f, left=p, color=S.TINT["blocker"], edgecolor=S.ROLE["blocker"], hatch=S.HATCH["blocker"], label="finding" if i == 0 else None)
    ax.text(int(n) + 0.2, i, f"{p} + {f}", va="center", fontsize=9)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis(); ax.set_xlim(0, 12)
ax.set_xlabel("questions"); ax.legend(loc="lower right", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 8, data="04-code/ch32/output/triage.txt, review.txt")
