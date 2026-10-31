"""Figure 32.2: questionnaire size at three customers: asked, applicable, design-changing."""
import re
import numpy as np
from _common import S, save, text
rows = re.findall(r"^  (\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+applicable", text("triage"), re.M)
fig, ax = S.figure(height=3.9)
x = np.arange(len(rows)); w = 0.26
for i, (nm, r) in enumerate([("asked", "evidence"), ("applicable", "system"), ("can change the design", "blocker")]):
    v = [int(row[i + 1]) for row in rows]
    ax.bar(x + (i - 1) * w, v, w, color=S.ROLE[r] if i == 0 else S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r], label=nm)
    for a, b in zip(x + (i - 1) * w, v):
        ax.text(a, b + 1.5, str(b), ha="center", fontsize=9)
ax.set_xticks(x); ax.set_xticklabels([r[0] for r in rows]); ax.set_ylabel("questions"); ax.set_ylim(0, 125)
ax.legend(loc="upper left", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 2, data="04-code/ch32/output/triage.txt")
