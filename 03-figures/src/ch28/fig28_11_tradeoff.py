"""Figure 28.11: six policy packs: attacks stopped against clean work that reaches the queue."""
import re
from _common import S, save, text
t = text("tradeoff")
rows = re.findall(r"^(P\d) .*?\s+\d+\s+(\d+)/140\s+(\d+)/166", t, re.M)
fig, ax = S.figure(height=4.2)
offs = {"P0": (6, -14), "P1": (6, 6), "P2": (6, -12), "P3": (-22, -16), "P4": (8, 0), "P5": (8, -4)}
for p, s, q in rows:
    x, y = int(s) / 140 * 100, int(q) / 166 * 100
    r = "approval" if p == "P3" else "evidence"
    ax.scatter(x, y, s=60 if p == "P3" else 36, color=S.ROLE[r], zorder=3)
    ax.annotate(p, (x, y), textcoords="offset points", xytext=offs[p], fontsize=10)
ax.set_xlabel("attacks stopped (%)"); ax.set_ylabel("benign work reaching the queue (%)")
ax.set_xlim(40, 105); ax.set_ylim(60, 103); ax.spines[["top", "right"]].set_visible(False)
save(fig, 11, data="04-code/ch28/output/tradeoff.txt")
