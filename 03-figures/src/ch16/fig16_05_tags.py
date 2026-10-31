"""Figure 16.5: field accuracy on the real 200 by exception tag; every tag lands below the untagged documents."""
from _common import S, save, tag_table
fig, ax = S.figure(height=4.2)
rows = tag_table()[::-1]
for y, (t, n, a) in enumerate(rows):
    role = "evidence" if t == "no exception" else "cost"
    ax.barh(y, a, color=S.TINT[role], edgecolor=S.ROLE[role], hatch=S.HATCH[role], lw=S.LW["data"], height=0.6)
    ax.text(a + 1, y, f"{a}%  ({n} docs)", va="center", fontsize=9)
ax.axvline(94.1, color=S.ROLE["data"], lw=S.LW["control"], ls="--")
ax.text(93.4, len(rows) - 0.4, "synthetic 94%", ha="right", fontsize=9, color=S.PAL["ink"])
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=9.5)
ax.set_xlim(0, 112); ax.set_xticks([0, 25, 50, 75, 100]); ax.set_xlabel("field accuracy on the real sample (%)")
save(fig, 5, data="04-code/ch16/output/failure_no_exceptions.txt")
