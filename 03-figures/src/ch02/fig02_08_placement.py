"""Figure 2.8: Where Experts Disagree. The same Caldwell year one with FDE cost above and below the gross-margin line."""
from _common import S, save, title, FIGSIZE
import matplotlib.pyplot as plt
from contracts import CONTRACTS, FIELD_ESTIMATE
from margin import year_one

y = year_one(CONTRACTS["caldwell"], FIELD_ESTIMATE["caldwell"])
above = y.margin * 100
below = (y.revenue - y.run_cost - y.cogs) / y.revenue * 100
fig, ax = plt.subplots(figsize=FIGSIZE)
for i, (v, lab, role) in enumerate([(above, "FDE hours in cost of revenue", "cost"), (below, "FDE hours below the line\n(sales or R&D)", "evidence")]):
    ax.barh(i, v, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white", height=0.5)
    ax.text(v + 1, i, f"{v:.0f}% gross margin", va="center", fontsize=9.5)
ax.set_yticks([0, 1]); ax.set_yticklabels(["in cost of revenue", "below the line\n(sales or R&D)"], fontsize=9.5)
ax.set_xlim(0, 110); ax.set_ylim(1.5, -0.8); ax.set_xlabel("year-one gross margin, %")
ax.text(1, -0.55, f"same engagement, same ${y.fde_cost/1e3:,.0f}k of FDE hours; only the line moves", fontsize=9, color=S.PAL["slate"])
title(ax, "Caldwell Mutual: one engagement, two gross margins")
save(fig, 8)
