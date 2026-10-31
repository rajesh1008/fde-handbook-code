"""Figure 42.1: Pennant's first ninety days, production day 0 to Live Stable (lab calendar, world.CAL)."""
from _common import S, save, blank
fig, ax = S.figure(height=4.9); blank(ax, (-4, 94), (0, 10))
ax.axvspan(45, 75, ymin=0.38, ymax=0.62, color=S._mix(S.ROLE["cost"], 0.25), lw=0)
ax.text(60, 3.4, "change freeze", ha="center", fontsize=9, color=S.PAL["ink"])
ax.plot([0, 90], [5, 5], color=S.PAL["grey"], lw=1.5)
ev = [(0, 2, "go-live", "system", 1), (14, 13, "sponsor\nleaves", "blocker", 1),
      (19, 26, "layout\ndrift", "data", 1), (33, 39.5, "re-calibration\nsigned", "approval", 1),
      (38, 6, "02:10\npage", "blocker", -1), (41, 20, "deprecation\nnotice", "cost", -1),
      (55, 35, "EU model\nmigrated", "model", -1), (70, 56, "drill\nalone", "evidence", 1),
      (90, 85, "Live\nStable", "approval", 1), (62, 72, "pin\nretires", "cost", -1)]
for d, cx, t, r, side in ev:
    y = 6.6 if side > 0 else 0.6
    ax.plot([d, cx], [5, y if side > 0 else y + 2.6], color=S.PAL["grey"], lw=0.75)
    S.box(ax, cx - 5.5, y, 11, 2.6, t, role=r, fs=9.5)
    ax.plot(d, 5, "o", color=S.ROLE[r], ms=6)
for d in range(0, 91, 15):
    ax.text(d, 4.1, f"{d}", ha="center", fontsize=9, color=S.PAL["ink"])
save(fig, 1, kind="diagram", data="04-code/ch42/world.py CAL; output/replay_v1.txt, drill_v0.txt, deprecation_v1.txt")
