"""Figure 9.8: share of documents with every step right, against the number of model-decided steps."""
from _common import S, save, plt
fig, ax = S.figure(3.9)
ns = list(range(1, 13))
for p, r in ((0.99, "system"), (0.97, "data"), (0.95, "cost"), (0.90, "blocker")):
    ax.plot(ns, [p ** n for n in ns], color=S.ROLE[r], lw=S.LW["emphasis"], marker="o", ms=3.5, label=f"{p:.2f} per step")
ax.annotate(f"demo agent: 12 steps at 0.97 = {0.97 ** 12:.0%}", xy=(12, 0.97 ** 12), xytext=(4.2, 0.42), fontsize=9.5,
            arrowprops=dict(arrowstyle="-|>", color=S.PAL["ink"], lw=1))
ax.set_xlabel("steps decided by a model"); ax.set_ylabel("documents with every step right")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}")); ax.set_ylim(0.2, 1.02); ax.set_xticks([1, 3, 5, 7, 9, 12])
ax.legend(fontsize=9, frameon=False, loc="lower left")
save(fig, 8)
