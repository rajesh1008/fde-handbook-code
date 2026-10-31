"""Figure 2.1: Caldwell's reconstructed hours ledger, weeks 1 to 7, by bucket."""
from _common import S, save, title, FIGSIZE
import matplotlib.pyplot as plt
from hours_ledger import LEDGER, BUCKETS

ROLEOF = dict(discovery="data", access="blocker", model="model", integration="system", gates="approval",
              handover="evidence", blocked="cost")
fig, ax = plt.subplots(figsize=FIGSIZE)
weeks = sorted({w for w, _, _ in LEDGER})
bottom = [0] * len(weeks)
for b in BUCKETS:
    vals = [sum(h for w, bb, h in LEDGER if w == wk and bb == b) for wk in weeks]
    if not any(vals):
        continue
    r = ROLEOF[b]
    ax.bar(weeks, vals, bottom=bottom, color=S.ROLE[r], hatch=S.HATCH[r] or {"blocked": "oo", "gates": "++"}.get(b, ""),
           edgecolor="white", label=b, width=0.65)
    bottom = [x + v for x, v in zip(bottom, vals)]
ax.set_xticks(weeks); ax.set_xticklabels([f"wk {w}" for w in weeks])
ax.set_ylabel("FDE hours (two engineers)")
ax.legend(frameon=False, fontsize=9, ncol=3, loc="upper left")
ax.set_ylim(0, 120)
title(ax, "Caldwell Mutual, days 1 to 47, rebuilt from calendars and commits")
save(fig, 1)
