"""Figure 10.1: Pennant's integration tax as each estimate was written: deal sheet, Chapter 2 field estimate,
day 21 (assumed TMS API) and day 24 (after the architects' answer), with the day-24 P10 to P90 range."""
from _common import S, plt, save, quiet
with quiet():
    from inventories import pennant
d21, d24 = pennant(denied=False), pennant(); e = d24.simulate()
labels = ["deal sheet", "field estimate\n(Chapter 2)", "day 21\n(API assumed)", "day 24\n(CSV priced)"]
vals = [0.50, 2.00, d21.point_tax(), d24.point_tax()]
roles = ["cost", "evidence", "blocker", "system"]
fig, ax = S.figure(3.8)
for i, (v, r) in enumerate(zip(vals, roles)):
    ax.bar(i, v, color=S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r], width=0.6, linewidth=S.LW["control"])
    ax.text(i - 0.32, v + 0.08, f"{v:.2f}", ha="right", fontsize=9.5)
ax.plot([3, 3], [e.tax.p10, e.tax.p90], color=S.PAL["ink"], lw=S.LW["emphasis"])
for y in (e.tax.p10, e.tax.p90): ax.plot([2.9, 3.1], [y, y], color=S.PAL["ink"], lw=S.LW["control"])
ax.text(3.36, e.tax.p90, f"P90 {e.tax.p90:.2f}", va="center", fontsize=9)
ax.text(3.36, e.tax.p10, f"P10 {e.tax.p10:.2f}", va="center", fontsize=9)
ax.set_xticks(range(4)); ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel("integration hours per model hour"); ax.set_ylim(0, 4.2); ax.set_xlim(-0.6, 4.0)
save(fig, 1)
