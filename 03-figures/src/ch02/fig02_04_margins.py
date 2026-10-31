"""Figure 2.4: year-one margin, deal sheet against field estimate, with the 60% target."""
from _common import S, save, title, SHORT, FIGSIZE
import matplotlib.pyplot as plt
from contracts import CONTRACTS, DEAL_SHEET, FIELD_ESTIMATE
from margin import year_one

fig, ax = plt.subplots(figsize=FIGSIZE)
for i, k in enumerate(CONTRACTS):
    for j, (plans, role, lab) in enumerate([(DEAL_SHEET, "evidence", "deal sheet"), (FIELD_ESTIMATE, "cost", "field estimate")]):
        m = year_one(CONTRACTS[k], plans[k]).margin
        ax.bar(i + (j - 0.5) * 0.36, m * 100, width=0.34, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white",
               label=lab if i == 0 else None)
        ax.text(i + (j - 0.5) * 0.36, m * 100 + 1.5, f"{m:.0%}", ha="center", fontsize=9)
ax.axhline(60, color=S.ROLE["approval"], ls="--", lw=1.4)
ax.text(1.42, 61.5, "target 60%", ha="center", fontsize=9, color=S.PAL["ink"])
ax.set_xticks(range(3)); ax.set_xticklabels([SHORT[k] for k in CONTRACTS])
ax.set_ylabel("year-one gross margin, %"); ax.set_ylim(0, 85); ax.legend(frameon=False, loc="upper right", fontsize=9)
title(ax, "The deal sheet and the field estimate disagree by 9 to 69 points")
save(fig, 4)
