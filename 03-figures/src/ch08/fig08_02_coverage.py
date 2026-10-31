"""Figure 8.2: where Caldwell's 14,800 monthly documents go under the signed scope."""
from _common import S, plt, save
import caldwell_scope as cs
doc = cs.signed()
rows = [(t.name, t.volume, "system") for t in doc.doc_types] + [(e.item, e.volume, "evidence") for e in doc.exclusions]
rows.sort(key=lambda r: r[1])
fig, ax = S.figure(4.6)
for i, (n, v, r) in enumerate(rows):
    ax.barh(i, v, color=S.ROLE[r], hatch=S.HATCH[r], edgecolor="white", height=0.65)
    ax.text(v + 60, i, f"{v:,}", va="center", fontsize=9)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=9)
ax.set_xlabel("documents a month (in scope: solid teal; out: slate cross-hatch)")
ax.set_xlim(0, 6000)
save(fig, 2)
