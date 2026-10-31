"""Figure 43.2: what Pennant pays for operations, cumulative by month, four paths. Data: model_pennant.txt."""
from itertools import accumulate
from _common import S, save, months, PATH_STYLE
d = months("pennant")
fig, ax = S.figure(height=3.9)
for k, (role, ls, lab) in PATH_STYLE.items():
    c = [v / 1000 for v in accumulate(d[k]["customer"])]
    ax.plot(range(1, 25), c, color=S.ROLE[role], ls=ls, lw=S.LW["emphasis"] if k == "managed" else S.LW["control"])
    ax.text(24.4, c[-1], lab, fontsize=9, va="center", color=S.PAL["ink"])
ax.axvline(12.5, color=S.PAL["grey"], lw=S.LW["data"])
ax.set_xlim(0.5, 33); ax.set_xticks([1, 6, 12, 18, 24])
ax.set_xlabel("month of the model"); ax.set_ylabel("cumulative cost, $ thousands")
save(fig, 2, data="04-code/ch43/output/model_pennant.txt (MONTHS)")
