"""Figure 30.4: accuracy by document kind on Anne's set, c06-ft1 with guard vs c06-p4 (Listing 30.2)."""
from _common import S, save, text, nums
lines = text("compare").splitlines()
i = [k for k, l in enumerate(lines) if l.startswith("kind (true class)")][0]
rows = []
for l in lines[i + 1:i + 11]:
    name = l[:28].strip(); n = nums(l[28:]); rows.append((name, int(n[0]), n[1], n[2]))
fig, ax = S.figure(height=5.6)
for j, (name, n, a, b) in enumerate(rows):
    ax.barh(j - 0.2, a, 0.38, color=S.ROLE["system"], hatch=S.HATCH["system"], edgecolor="white")
    ax.barh(j + 0.2, b, 0.38, color=S.ROLE["model"])
ax.set_yticks(range(len(rows)), [f"{r[0]} ({r[1]})" for r in rows], fontsize=9); ax.invert_yaxis()
ax.set_xlim(0, 100); ax.set_xlabel("typed right (%)")
for j, (name, n, a, b) in enumerate(rows):
    if a < 60 or b < 60:
        S.label(ax, max(a, b) + 1.5, j + 0.1, f"{a:.0f}% vs {b:.0f}%", va="center", fs=9)
S.label(ax, 2, -1.1, "c06-ft1 + guard", color=S.ROLE["system"], fs=9)
S.label(ax, 40, -1.1, "c06-p4", color=S.ROLE["model"], fs=9)
ax.set_ylim(len(rows) - 0.5, -1.5)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 4, data="04-code/ch30/output/compare.txt")
