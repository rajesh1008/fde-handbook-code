"""Figure 2.7: the failure injection. T&M assumed on a fixed-price contract."""
from _common import S, save, title, FIGSIZE
import matplotlib.pyplot as plt
from contracts import CONTRACTS, FIELD_ESTIMATE
from margin import year_one, with_

c = CONTRACTS["pennant"]; p = with_(FIELD_ESTIMATE["pennant"], integration_tax=3.0)
wrong = year_one(c, p, assume_billing="tm", strict=False); right = year_one(c, p)
fig, ax = plt.subplots(figsize=FIGSIZE)
for i, (y, lab, role) in enumerate([(wrong, "forecast: T&M assumed", "blocker"), (right, "contract: fixed price", "cost")]):
    ax.bar(i - 0.2, y.revenue / 1e3, width=0.38, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white")
    ax.bar(i + 0.2, y.cost / 1e3, width=0.38, color=S.PAL["mist"], edgecolor=S.PAL["ink"], hatch="xx")
    ax.text(i - 0.2, y.revenue / 1e3 + 25, f"revenue\n${y.revenue/1e3:,.0f}k", ha="center", fontsize=9)
    ax.text(i + 0.2, y.cost / 1e3 + 25, f"cost\n${y.cost/1e3:,.0f}k", ha="center", fontsize=9)
    ax.text(i, -170, f"margin {y.margin:.0%}", ha="center", fontsize=10, fontweight="bold")
ax.set_xticks([0, 1]); ax.set_xticklabels(["forecast: T&M assumed", "contract: fixed price"])
ax.set_ylim(-230, 1700); ax.axhline(0, color=S.PAL["ink"], lw=0.8)
ax.set_ylabel("US dollars, thousands")
title(ax, "Pennant Logistics at an integration tax of 3: same hours, two margins")
save(fig, 7)
