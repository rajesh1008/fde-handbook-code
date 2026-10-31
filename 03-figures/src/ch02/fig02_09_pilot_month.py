"""Figure 2.9: what one more month before production costs, by component."""
from _common import S, save, title, SHORT, FIGSIZE
import matplotlib.pyplot as plt
from contracts import CONTRACTS, FIELD_ESTIMATE
from margin import pilot_month_cost

fig, ax = plt.subplots(figsize=FIGSIZE)
parts = [("fde_cost", "FDE burn", "cost"), ("run", "model and hosting", "model"), ("deferred_subscription", "subscription not yet billing", "blocker")]
for i, k in enumerate(CONTRACTS):
    d = pilot_month_cost(CONTRACTS[k], FIELD_ESTIMATE[k]); left = 0
    for key, lab, role in parts:
        ax.barh(i, d[key] / 1e3, left=left, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white",
                label=lab if i == 0 else None, height=0.55)
        left += d[key] / 1e3
    ax.text(left + 3, i, f"${d['total']/1e3:,.1f}k a month", va="center", fontsize=9)
ax.set_yticks(range(3)); ax.set_yticklabels([SHORT[k] for k in CONTRACTS])
ax.set_xlabel("US dollars, thousands per month"); ax.set_xlim(0, 290); ax.invert_yaxis()
ax.legend(frameon=False, fontsize=9, loc="lower right")
title(ax, "One more pilot month: the subscription clause dominates")
save(fig, 9)
