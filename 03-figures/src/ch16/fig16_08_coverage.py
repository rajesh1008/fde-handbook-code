"""Figure 16.8: exception coverage; v1 has none of the four common exceptions, v2 has each within a few points."""
from _common import S, save, coverage_table
fig, ax = S.figure(height=4.0)
v1, v2 = coverage_table()
rows = [r for r in v1 if r[1] >= 2]
w = 0.26
for i, (t, real, s1) in enumerate(rows):
    s2 = dict((a, c) for a, _, c in v2)[t]
    for k, (v, role, lab) in enumerate(((real, "data", "real 200"), (s1, "cost", "synthetic v1"), (s2, "evidence", "synthetic v2"))):
        x = i + (k - 1) * w
        ax.bar(x, max(v, 0.4), width=w, color=S.TINT[role], edgecolor=S.ROLE[role], hatch=S.HATCH[role],
               lw=S.LW["data"], label=lab if i == 0 else None)
        ax.text(x, max(v, 0.4) + 1.2, f"{v}", ha="center", fontsize=9)
ax.set_xticks(range(len(rows))); ax.set_xticklabels([r[0].replace(" or ", " or\n").replace("a first", "a\nfirst") for r in rows], fontsize=9.5)
ax.set_ylim(0, 92); ax.set_ylabel("share of documents (%)")
ax.legend(frameon=True, edgecolor=S.PAL["light"], fontsize=9, loc="upper right")
save(fig, 8, data="04-code/ch16/output/represent.txt")
