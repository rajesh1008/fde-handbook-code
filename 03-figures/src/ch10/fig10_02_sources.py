"""Figure 10.2: most-likely integration hours by source for the three customers, against model work hours."""
from _common import S, plt, save, quiet
with quiet():
    from inventories import ALL
    from fieldkit.integration import SOURCES
roles = dict(access="blocker", identity="evidence", formats="data", exceptions="cost", environments="system", gateways="model")
cust = list(ALL); invs = [ALL[k]() for k in cust]
fig, ax = S.figure(3.8)
left = [0] * 3
for s in SOURCES:
    v = [i.by_source()[s] for i in invs]
    ax.barh(range(3), v, left=left, color=S.TINT[roles[s]], edgecolor=S.ROLE[roles[s]], hatch=S.HATCH[roles[s]] or None,
            linewidth=S.LW["data"], label=s, height=0.55)
    left = [a + b for a, b in zip(left, v)]
for y, i in enumerate(invs):
    m = i.model_hours[1]
    ax.plot([m, m], [y - 0.36, y + 0.36], color=S.PAL["ink"], lw=S.LW["emphasis"])
    ax.text(max(left[y], m) + 25, y, f"{i.total():,.0f} h, tax {i.point_tax():.2f}", va="center", fontsize=9)
ax.text(invs[0].model_hours[1] + 15, -0.42, "model work (most likely)", fontsize=9)
ax.set_yticks(range(3)); ax.set_yticklabels([i.customer for i in invs], fontsize=9.5)
ax.set_xlabel("most-likely hours"); ax.set_xlim(0, 2050); ax.set_ylim(2.5, -0.65); 
ax.legend(ncol=6, fontsize=9, loc="upper center", bbox_to_anchor=(0.45, -0.2), frameon=False, handlelength=1.2, columnspacing=0.8)
save(fig, 2)
