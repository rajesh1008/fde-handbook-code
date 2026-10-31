"""Figure 2.5: anatomy of Caldwell's year one, field estimate, as a waterfall from revenue to gross profit."""
from _common import S, save, title, FIGSIZE
import matplotlib.pyplot as plt
from contracts import CONTRACTS, FIELD_ESTIMATE
from margin import year_one

y = year_one(CONTRACTS["caldwell"], FIELD_ESTIMATE["caldwell"])
steps = [("subscription", y.subscription, "system"), ("deployment fee", y.services, "system"),
         ("FDE hours", -y.fde_cost, "cost"), ("model and hosting", -y.run_cost, "model"),
         ("product support share", -y.cogs, "evidence")]
fig, ax = plt.subplots(figsize=FIGSIZE)
level = 0
for i, (lab, v, role) in enumerate(steps):
    bottom = level if v > 0 else level + v
    ax.bar(i, abs(v), bottom=bottom, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white", width=0.6)
    ax.text(i, bottom + abs(v) + 25_000, f"{'+' if v > 0 else '-'}${abs(v)/1e3:,.0f}k", ha="center", fontsize=9)
    level += v
ax.bar(len(steps), level, color=S.ROLE["approval"], width=0.6, edgecolor="white")
ax.text(len(steps), level + 25_000, f"${level/1e3:,.0f}k\n{y.margin:.0%} margin", ha="center", fontsize=9)
ax.set_xticks(range(len(steps) + 1))
ax.set_xticklabels([s[0] for s in steps] + ["gross profit"], fontsize=9, rotation=15)
ax.set_ylabel("US dollars, year one"); ax.set_ylim(0, 2_150_000)
ax.yaxis.set_major_formatter(lambda v, _: f"${v/1e6:.1f}M")
title(ax, "Caldwell Mutual, year one, field estimate (illustrative)")
save(fig, 5)
