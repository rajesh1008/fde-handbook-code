"""Figure 10.6: Pennant's day-24 tax as 20,000 seeded draws, with P10, P50, P90 and the sum of most-likely lines."""
from _common import S, plt, save, quiet
import random
with quiet():
    from inventories import pennant
inv = pennant(); e = inv.simulate(); rng = random.Random(10); ts = []
ml, mm, mh = inv.model_hours
for _ in range(20000):
    h = sum(rng.triangular(l.low, l.stretched_high, l.likely) for l in inv.lines); ts.append(h / rng.triangular(ml, mh, mm))
fig, ax = S.figure(3.8)
ax.hist(ts, bins=60, color=S.TINT["system"], edgecolor=S.ROLE["system"], linewidth=0.5)
for x, lab, ls, lw in ((e.tax.p10, "P10", "--", "control"), (e.tax.p50, "P50", "-", "emphasis"), (e.tax.p90, "P90", "--", "control")):
    ax.axvline(x, color=S.PAL["ink"], ls=ls, lw=S.LW[lw]); ax.text(x + (0.02 if lab != "P10" else -0.02), ax.get_ylim()[1] * 0.95, f"{lab} {x:.2f}", fontsize=9, ha="left" if lab != "P10" else "right")
ax.axvline(e.point_tax, color=S.ROLE["blocker"], ls=":", lw=S.LW["emphasis"])
ax.text(e.tax.p10 - 0.03, ax.get_ylim()[1] * 0.5, f"sum of most-likely\nlines {e.point_tax:.2f}", ha="right", fontsize=9)
ax.set_xlabel("integration tax (integration hours per model hour)"); ax.set_ylabel("draws"); ax.set_xlim(2.3, 4.6)
save(fig, 6)
