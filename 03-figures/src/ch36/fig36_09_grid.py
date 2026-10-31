"""Figure 36.9: the eleven new findings on the likelihood-by-impact grid agreed before the attack days."""
from _common import S, save, text
from matplotlib.patches import Rectangle
from collections import defaultdict
cells = defaultdict(list)
for l in text("triage").splitlines():
    if l.startswith("F-") and "x" in l.split()[2]:
        li, im = l.split()[2].split("=")[0].split("x"); cells[(int(li), int(im))].append(l.split()[0])
assert sum(len(v) for v in cells.values()) == 11
fig, ax = S.figure(height=4.6)
for l in range(1, 6):
    for i in range(1, 6):
        s = l * i; r = "blocker" if s >= 12 else ("data" if s >= 6 else "evidence")
        ax.add_patch(Rectangle((i - 0.5, l - 0.5), 1, 1, facecolor=S.TINT[r], edgecolor="white", lw=2))
        ids = cells.get((l, i), [])
        if ids:
            ax.text(i, l, "\n".join(ids), ha="center", va="center", fontsize=9.5)
ax.set_xlim(0.5, 5.5); ax.set_ylim(0.5, 5.5); ax.set_aspect("auto")
ax.set_xticks(range(1, 6)); ax.set_yticks(range(1, 6))
ax.set_xlabel("impact"); ax.set_ylabel("likelihood")
ax.text(5.45, 5.42, "high: 12 and above", ha="right", va="top", fontsize=9.5,
        bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))
save(fig, 9, data="04-code/ch36/output/triage.txt")
