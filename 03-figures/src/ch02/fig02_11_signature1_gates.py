"""Figure 2.11 (Signature 1): the engagement timeline with five gates per customer, deal sheet against field estimate."""
from _common import S, save, title, SHORT, FIGSIZE
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from contracts import CONTRACTS, DEAL_SHEET, FIELD_ESTIMATE
from margin import gate_days, GATES

MARK = dict(zip(GATES, ["s", "D", "^", "P", "*"]))
fig, ax = plt.subplots(figsize=(S.WIDTH_IN, 4.4))
rows = []
for k in CONTRACTS:
    rows += [(k, DEAL_SHEET[k], "deal sheet"), (k, FIELD_ESTIMATE[k], "field estimate")]
for i, (k, p, lab) in enumerate(rows):
    y = len(rows) - 1 - i
    d = gate_days(p)
    field = lab == "field estimate"
    col = S.ROLE["cost"] if field else S.ROLE["evidence"]
    ax.plot([0, d["Live Stable"]], [y, y], color=col, lw=3 if field else 1.6, ls="-" if field else "--")
    for g in GATES:
        ax.plot(d[g], y, marker=MARK[g], ms=9 if g != "Live Stable" else 13, color=col,
                markeredgecolor="white", zorder=3)
    ax.text(d["Live Stable"] + 14, y, f"day {d['Live Stable']}", va="center", fontsize=9, color=S.PAL["ink"])
ax.axvline(270, color=S.ROLE["blocker"], lw=1.8, ls=":")
ax.text(272, len(rows) - 0.45, "month 9: live or stopped", fontsize=9, color=S.PAL["ink"])
ax.axvline(150, color=S.ROLE["approval"], lw=1.4, ls="-.")
ax.text(152, -0.95, "target: under 5 months", fontsize=9, color=S.PAL["ink"])
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([f"{SHORT[k]}, {lab}" for k, _, lab in reversed(rows)], fontsize=9)
ax.set_xlim(0, 380); ax.set_ylim(-1.3, len(rows) - 0.2); ax.set_xlabel("engagement day")
fig.legend(handles=[Line2D([], [], marker=MARK[g], ls="", color=S.PAL["ink"], label=g) for g in GATES],
           loc="outside lower center", fontsize=9, frameon=False, ncol=3)
title(ax, "Five gates per customer: the deal sheet against the field estimate")
save(fig, 11)
