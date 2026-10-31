"""Figure 40.1: the Chapter 40 calendar at Caldwell, live day 158 to audit report day 214 (evenly spaced, not to scale)."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9); blank(ax, (-0.6, 8.6), (0, 6))
ax.plot([-0.4, 8.4], [3, 3], color=S.PAL["ink"], lw=S.LW["control"])
ev = [(158, "live", "approval"), (166, "hotfix", "blocker"), (169, "disputed\ndecision", "evidence"),
      (176, "dispute", "evidence"), (177, "rehearsal", "blocker"), (180, "pinned", "system"),
      (184, "architects", "evidence"), ("201-210", "audit", "evidence"), (214, "report", "approval")]
for i, (d, t, r) in enumerate(ev):
    s = 1 if i % 2 == 0 else -1
    ax.plot([i, i], [3, 3 + 0.9 * s], color=S.ROLE[r], lw=S.LW["control"])
    ax.plot(i, 3, "o", color=S.ROLE[r], ms=7)
    S.label(ax, i, 3 + 1.05 * s, t, fs=10, ha="center", va="bottom" if s > 0 else "top")
    S.label(ax, i, 3 - 0.3 * s, f"day {d}" if i in (0, 8) else str(d), fs=9.5, ha="center", va="top" if s > 0 else "bottom")
save(fig, 1, kind="diagram", data="04-code/ch40/world.py (story calendar constants)")
