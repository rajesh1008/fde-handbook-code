"""Figure 11.4: days since last direct contact at day 40, against each person's limit, Greystone."""
from _common import S, save
import stakeholders as St, greystone as G
m = G.at_day(G.DAY12, G.CONTACT_DAY40, 40)
rows = [(p.name, 40 - p.last_contact, St.limit_for(p)) for p in m.people]
fig, ax = S.figure(3.9)
for i, (n, d, lim) in enumerate(rows):
    stale = d > lim
    r = "blocker" if stale else "system"
    ax.barh(i, d, height=0.6, color=S.ROLE[r] if not stale else S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r])
    ax.plot([lim, lim], [i - 0.4, i + 0.4], color=S.PAL["ink"], lw=S.LW["emphasis"])
    ax.text(d + 0.6, i, f"{d} days" + ("  stale" if stale else ""), va="center", fontsize=9.5)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis()
ax.set_xlim(0, 42); ax.set_xlabel("days since last direct contact (black tick: limit for the role)")
save(fig, 4)
