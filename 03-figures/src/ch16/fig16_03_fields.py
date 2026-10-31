"""Figure 16.3: per-field accuracy, synthetic v1 (self-scored) against the real 200 (keyed by Kessler's adjusters)."""
from _common import S, save, field_table
fig, ax = S.figure(height=4.4)
rows = sorted(field_table().items(), key=lambda kv: kv[1][0] - kv[1][1])
for y, (f, (s, r)) in enumerate(rows):
    ax.plot([r, s], [y, y], color=S.PAL["grey"], lw=S.LW["control"])
    ax.plot(s, y, "o", color=S.ROLE["data"], ms=7, mec=S.PAL["ink"], mew=0.75)
    ax.plot(r, y, "s", color=S.ROLE["cost"], ms=7, mec=S.PAL["ink"], mew=0.75)
    ax.text(r - 2, y, f"{r}", ha="right", va="center", fontsize=9)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([f.replace("_", " ") for f, _ in rows], fontsize=9.5)
ax.set_xlim(30, 104); ax.set_xlabel("field accuracy (%)")
ax.plot([], [], "o", color=S.ROLE["data"], mec=S.PAL["ink"], label="synthetic v1, 600 documents")
ax.plot([], [], "s", color=S.ROLE["cost"], mec=S.PAL["ink"], label="real sample, 200 documents")
ax.legend(loc="lower left", frameon=True, edgecolor=S.PAL["light"], fontsize=9)
save(fig, 3, data="04-code/ch16/output/failure_no_exceptions.txt")
