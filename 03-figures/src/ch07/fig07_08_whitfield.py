"""Figure 7.8: what the agent needs against what Tom Whitfield may do; the two gaps and their owners."""
from _common import S, plt, save, clean, quiet
with quiet():
    import whitfield as W
fig, ax = S.figure(3.9); clean(ax)
for i, n in enumerate(W.NEEDS):
    y = 6.1 - i * 1.0
    ok = n in W.GRANTS["Tom Whitfield (senior adjuster)"]
    S.box(ax, 0.2, y, 5.6, 0.8, n, role="system" if ok else "blocker", fs=10)
    ax.text(6.1, y + 0.4, "permitted" if ok else ("service desk" if "name" in n else "security lead"),
            va="center", fontsize=10)
save(fig, 8, kind="diagram")
