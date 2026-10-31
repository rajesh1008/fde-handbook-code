"""Figure 9.12: cost per document against the frontier steps left in a twelve-step pipeline."""
from _common import S, save, plt
import costs as K
_, demo = K.demo_cost("scan")
fs = [0, 1, 2, 3, 4]; vals = [K.pipeline_cost([10 - f, 0, 2, f], "scan")[1] * 100 for f in fs]
fig, ax = S.figure(3.9)
ax.plot(fs, vals, color=S.ROLE["model"], lw=S.LW["emphasis"], marker="o")
ax.axhline(demo * 100, color=S.ROLE["cost"], lw=S.LW["control"], ls="--"); ax.text(0, demo * 100 + 0.6, "demo agent", fontsize=9.5)
for f, lab in ((1, "Caldwell"), (2, "Greystone")):
    ax.annotate(lab, xy=(f, vals[f]), xytext=(f - 0.15, vals[f] + 4.2), fontsize=9.5, ha="right",
                arrowprops=dict(arrowstyle="-|>", color=S.PAL["ink"], lw=1))
ax.set_xticks(fs); ax.set_xlabel("frontier-model steps left (of 12)"); ax.set_ylabel("cents per scanned document")
ax.set_ylim(0, 21)
save(fig, 12)
