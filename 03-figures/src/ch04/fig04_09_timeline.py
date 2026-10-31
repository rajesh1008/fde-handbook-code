"""Figure 4.9: the five gates three ways: deal sheet, field estimate and the re-baselined ranges (rebaseline.py).
Gate markers match Signature 1 (Figure 2.11)."""
from _common import S, save, title
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from rebaseline import GATES, DEAL_SHEET, FIELD_ESTIMATE, REBASELINED, PROMISED_LIVE

MARK = dict(zip(GATES, ["s", "D", "^", "P", "*"]))
fig, ax = plt.subplots(figsize=(S.WIDTH_IN, 4.4))
for y, days, col in ((4.6, DEAL_SHEET, S.ROLE["evidence"]), (3.6, FIELD_ESTIMATE, S.ROLE["cost"])):
    ax.plot([0, days[-1]], [y, y], color=col, lw=1.4, ls="--" if y > 4 else "-")
    for g, d in zip(GATES, days):
        ax.plot(d, y, marker=MARK[g], ms=9 if g != "Live Stable" else 12, color=col, markeredgecolor="white", zorder=3)
for i, (g, lo, hi, _, _) in enumerate(REBASELINED):
    y = 2.6 - i * 0.42
    ax.barh(y, hi - lo, left=lo, height=0.3, color=S.TINT["approval"], edgecolor=S.ROLE["approval"], lw=1.2)
    ax.plot((lo + hi) / 2, y, marker=MARK[g], ms=8, color=S.ROLE["approval"], markeredgecolor="white", zorder=3)
    ax.text(hi + 4, y, f"{lo} to {hi}", va="center", fontsize=9)
ax.axvline(PROMISED_LIVE, color=S.PAL["ink"], lw=1.2, ls=":")
ax.text(PROMISED_LIVE + 3, 5.15, "promised: under five months", fontsize=9)
ax.set_yticks([4.6, 3.6, 1.76], ["deal sheet", "field estimate", "re-baselined,\nday 12"], fontsize=9)
ax.set_xlim(0, 300); ax.set_ylim(0.6, 5.5); ax.set_xlabel("engagement day")
fig.legend(handles=[Line2D([], [], marker=MARK[g], ls="", color=S.PAL["ink"], label=g) for g in GATES],
           loc="outside lower center", fontsize=9, frameon=False, ncol=3)
title(ax, "Five gates, three ways")
save(fig, 9, data="04-code/ch04/rebaseline.py (deal sheet and field estimate carried forward from Chapter 2)")
