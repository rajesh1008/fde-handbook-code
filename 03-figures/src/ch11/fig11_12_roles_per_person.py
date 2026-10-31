"""Figure 11.12: roles held per person across the three working maps, with the limit of three."""
from _common import S, save
import greystone as G, caldwell, pennant
rows = []
for cust, m in (("Greystone", G.DAY12), ("Caldwell", caldwell.DAY25), ("Pennant", pennant.DAY28)):
    for p in m.people:
        if p.roles:
            rows.append((f"{p.name.split(' (')[0]} ({cust})", len(p.roles)))
rows.sort(key=lambda r: -r[1])
fig, ax = S.figure(4.4)
for i, (n, k) in enumerate(rows):
    r = "blocker" if k > 3 else "evidence"
    ax.barh(i, k, height=0.62, color=S.TINT[r] if k <= 3 else S.ROLE[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r])
ax.axvline(3, color=S.PAL["ink"], lw=S.LW["control"], ls="--"); ax.text(3.08, len(rows) - 0.6, "limit", fontsize=9.5)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=9.5); ax.invert_yaxis()
ax.set_xlim(0, 5); ax.set_xticks(range(6)); ax.set_xlabel("roles held of five")
save(fig, 12)
