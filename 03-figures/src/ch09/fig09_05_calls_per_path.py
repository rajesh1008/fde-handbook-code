"""Figure 9.5: model calls per document on each intake path, bar width-coded by monthly volume in the label."""
from _common import S, save, plt
from intake_paths import walk_paths
rows = [(row[0], row[2], c[2] + c[3]) for row, _, c, _ in walk_paths()]
fig, ax = S.figure(3.9)
cols = [S.ROLE["model"] if n == 3 else S.ROLE["data"] if n else S.ROLE["system"] for _, _, n in rows]
ax.bar(range(len(rows)), [n for *_, n in rows], color=cols, edgecolor="white")
for i, (_, v, n) in enumerate(rows): ax.text(i, n + 0.08, str(n), ha="center", fontsize=10)
ax.set_xticks(range(len(rows))); ax.set_xticklabels([p for p, *_ in rows], fontsize=9)
ax.set_ylim(0, 3.8); ax.set_ylabel("model calls per document"); ax.set_yticks([0, 1, 2, 3])
tot = sum(v for _, v, _ in rows); avg = sum(v * n for _, v, n in rows) / tot
ax.axhline(avg, color=S.PAL["ink"], lw=S.LW["control"], ls="--")
ax.text(10.4, avg + 0.1, f"weighted {avg:.2f}", ha="right", fontsize=9.5)
save(fig, 5)
