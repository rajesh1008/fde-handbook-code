"""Figure 7.5: late-arriving facts. Share of gold loss dates later corrected, by the record's age when taken."""
from _common import S, plt, save
from caldwell_records import loss_date_corrections
c = loss_date_corrections(); ages = list(range(0, 31))
v = [100 * sum(1 for x in c if x is not None and x > a) / len(c) for a in ages]
fig, ax = S.figure(3.8)
ax.plot(ages, v, color=S.ROLE["data"], lw=S.LW["emphasis"])
ax.axvline(14, color=S.ROLE["approval"], lw=S.LW["control"], ls="--")
ax.text(14.5, 8, "rule after day 24:\nrecords 14+ days old", fontsize=9)
ax.text(1, v[0] + 0.3, f"{v[0]:.1f}% at age 0", fontsize=9)
ax.set_xlabel("age of claim record when the gold value is taken (days)")
ax.set_ylabel("gold values later corrected (%)"); ax.set_ylim(0, 11)
save(fig, 5)
