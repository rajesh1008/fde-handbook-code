"""Figure 2.12: Pennant staffing trade-off; more engineers lower year-one margin and raise renewal odds."""
from _common import S, save, title, FIGSIZE
import matplotlib.pyplot as plt
from contracts import CONTRACTS, FIELD_ESTIMATE
from margin import year_one, with_, renewal_probability, two_year_gross_profit

c, base = CONTRACTS["pennant"], FIELD_ESTIMATE["pennant"]
fig, ax = plt.subplots(figsize=FIGSIZE)
for fte, mk in [(1.5, "o"), (2.0, "s"), (3.0, "D")]:
    p = with_(base, fde_fte=fte); y = year_one(c, p)
    g = two_year_gross_profit(c, p)["total"]
    ax.plot(y.margin * 100, renewal_probability(p.months_to_production) * 100, mk, ms=11, color=S.ROLE["cost"])
    ax.annotate(f"{fte} FDEs: {p.months_to_production:.1f} months\n2-yr GP ${g/1e3:,.0f}k", (y.margin * 100, renewal_probability(p.months_to_production) * 100),
                (y.margin * 100 + 0.4, renewal_probability(p.months_to_production) * 100 - 9), fontsize=9)
ax.set_xlabel("year-one gross margin, %"); ax.set_ylabel("renewal probability, %")
ax.set_xlim(35, 51); ax.set_ylim(40, 100)
title(ax, "Pennant Logistics: the cheapest staffing is the least likely to renew")
save(fig, 12)
