"""Figure 8.8: monthly cost lines in the signed scope, each labeled with its basis."""
from _common import S, plt, save
rows = [("manual intake, measured", 82194, "cost"), ("model ceiling, target", 4498, "evidence"),
        ("model estimate, vendor", 2361, "blocker")]
fig, ax = S.figure(3.7)
for i, (n, v, r) in enumerate(rows):
    ax.barh(i, v, color=S.ROLE[r], hatch=S.HATCH[r], edgecolor="white", height=0.6)
    ax.text(v * 1.15, i, f"${v:,}", va="center", fontsize=9.5)
ax.set_xscale("log"); ax.set_xlim(1000, 300000)
ax.set_yticks(range(3)); ax.set_yticklabels([r[0] for r in rows], fontsize=9.5); ax.invert_yaxis()
ax.set_xlabel("dollars a month, 11,244 in-scope documents (log scale)")
save(fig, 8)
