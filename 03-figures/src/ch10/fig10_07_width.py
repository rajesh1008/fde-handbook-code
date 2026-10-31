"""Figure 10.7: share of each customer's estimate width (stretched high minus low, summed) that sits on unconfirmed facts."""
from _common import S, plt, save, quiet
with quiet():
    from inventories import ALL
    from fieldkit.integration import UNCONFIRMED
fig, ax = S.figure(3.7); names = []
for y, k in enumerate(ALL):
    i = ALL[k](); w = sum(l.stretched_high - l.low for l in i.lines)
    u = sum(l.stretched_high - l.low for l in i.lines if l.status in UNCONFIRMED); names.append(i.customer)
    ax.barh(y, w, color="white", edgecolor=S.ROLE["evidence"], height=0.55, linewidth=S.LW["control"])
    ax.barh(y, u, color=S.TINT["blocker"], edgecolor=S.ROLE["blocker"], hatch=S.HATCH["blocker"], height=0.55)
    ax.text(w + 20, y, f"{u:,.0f} of {w:,.0f} h ({u / w:.0%})", va="center", fontsize=9)
ax.set_yticks(range(3)); ax.set_yticklabels(names, fontsize=9.5); ax.invert_yaxis()
ax.set_xlabel("range width in hours (hatched: on unconfirmed facts)"); ax.set_xlim(0, 1800)
save(fig, 7)
