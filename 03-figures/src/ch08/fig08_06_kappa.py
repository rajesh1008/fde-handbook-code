"""Figure 8.6: per-field kappa among three scorers before and after the day-25 alignment session."""
from _common import S, plt, save
import calibration as cal
r1, r2 = cal.per_field(1), cal.per_field(2)
order = sorted(range(14), key=lambda i: r2[i][1])
fig, ax = S.figure(5.2)
for y, i in enumerate(order):
    f, k1, _ = r1[i]; _, k2, _ = r2[i]
    ax.plot([k1, k2], [y, y], color=S.PAL["light"] if "light" in S.PAL else "#D9DEE4", lw=1.5)
    ax.plot(k1, y, "s", color=S.ROLE["evidence"], ms=5)
    ax.plot(k2, y, "o", color=S.ROLE["model"] if k2 >= .8 else S.ROLE["blocker"], ms=6)
ax.axvline(0.8, color=S.PAL["ink"], lw=0.75, ls="--")
ax.text(0.81, -0.9, "0.80 floor for an exact check", fontsize=9)
ax.set_yticks(range(14)); ax.set_yticklabels([r2[i][0] for i in order], fontsize=9, family="monospace")
ax.set_xlabel("kappa, mean of three scorer pairs (square: round 1; circle: round 2)")
ax.set_xlim(0.2, 1.05); ax.set_ylim(-1.5, 13.6)
save(fig, 6)
