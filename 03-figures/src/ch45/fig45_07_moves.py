"""Figure 45.7: the five-move check on three answers to the same discovery question."""
import re
import numpy as np
from matplotlib.colors import ListedColormap
from _common import S, save, text
MOVES = ("position", "evidence", "example", "boundary", "proof")
rows = [("weak answer", text("moves_weak")), ("strong answer, last two\nsentences removed", text("tryit_b")), ("strong answer", text("moves_strong"))]
m = np.array([[1 if re.search(rf"{k} yes", t) else 0 for k in MOVES] for _, t in rows])
fig, ax = S.figure(height=4.0)
ax.imshow(m, cmap=ListedColormap(["#FFFFFF", S.TINT["approval"]]), vmin=0, vmax=1, aspect="auto")
for i in range(m.shape[0]):
    for j in range(5):
        ax.text(j, i, "yes" if m[i, j] else "missing", ha="center", va="center", fontsize=10, color=S.PAL["ink"],
                fontweight="bold" if m[i, j] else "normal", bbox=dict(fc="white", ec="none", pad=1.0))
ax.set_xticks(range(5)); ax.set_xticklabels(MOVES); ax.xaxis.tick_top()
ax.set_yticks(range(3)); ax.set_yticklabels([f"{n}\n{int(m[i].sum())} of 5" for i, (n, _) in enumerate(rows)], fontsize=9.5)
ax.set_xticks([x - 0.5 for x in range(1, 5)], minor=True); ax.set_yticks([0.5, 1.5], minor=True)
ax.grid(which="minor", color=S.PAL["ink"], lw=0.5); ax.tick_params(which="both", length=0)
for s in ax.spines.values():
    s.set_visible(False)
save(fig, 7, data="04-code/ch45/output/moves_weak.txt, moves_strong.txt, tryit_b.txt")
