"""Figure 50.8: the same fourteen components under the vendor's reading and the bank's; five move to full scope."""
import re
import numpy as np
from matplotlib.colors import ListedColormap
from _common import S, save, text
lines = [l for l in text("classify").splitlines() if re.match(r"H\d\d ", l)]
val = {"not a model": 0, "registered, not validated": 1, "full scope": 2}
word = {0: "not a model", 1: "registered", 2: "full scope"}
rows = []
for l in lines:
    rows.append((l[:3], l[5:43].strip(), val[l[44:70].strip()], val[l[71:97].strip()]))
m = np.array([[r[2], r[3]] for r in rows])
fig, ax = S.figure(height=6.4)
ax.imshow(m, cmap=ListedColormap(["#FFFFFF", S.TINT["evidence"], S.TINT["blocker"]]), vmin=0, vmax=2, aspect="auto")
for i, r in enumerate(rows):
    for j in (0, 1):
        ax.text(j, i, word[m[i, j]], ha="center", va="center", fontsize=9.5, color=S.PAL["ink"],
                fontweight="bold" if (j == 1 and r[2] != r[3]) else "normal")
ax.set_xticks([0, 1]); ax.set_xticklabels(["vendor reading", "bank's reading"]); ax.xaxis.tick_top()
ax.set_yticks(range(len(rows))); ax.set_yticklabels([f"{r[0]} {r[1]}" for r in rows], fontsize=9)
ax.set_xticks([0.5], minor=True); ax.set_yticks([y + 0.5 for y in range(len(rows) - 1)], minor=True)
ax.grid(which="minor", color=S.PAL["ink"], lw=0.5); ax.tick_params(which="both", length=0)
for s in ax.spines.values():
    s.set_visible(False)
save(fig, 8, data="04-code/ch50/output/classify.txt")
