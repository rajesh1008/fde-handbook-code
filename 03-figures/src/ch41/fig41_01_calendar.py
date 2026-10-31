"""Figure 41.1: Caldwell's hand-over calendar, live on day 158 to the R2 report due on day 190."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9); blank(ax, (150, 194), (0, 6))
ax.plot([156, 192], [3, 3], color=S.PAL["ink"], lw=S.LW["control"])
ev = [(158, "live", "approval", 1), (160, "hand-over\nplan", "evidence", -1), (168, "reference v1", "evidence", 1),
      (176, "drill 1\nfails", "blocker", -1), (177, "A-07\nrerouted", "system", 1), (183, "drill 2\npasses, 0.90", "approval", -1),
      (190, "R2 report\ndue", "data", 1)]
for d, t, r, side in ev:
    ax.plot([d, d], [3, 3 + side * 0.9], color=S.ROLE[r], lw=S.LW["emphasis"])
    S.box(ax, d - 2.6, 3 + side * 0.9 + (0 if side > 0 else -1.3), 5.2, 1.3, t, role=r, fs=9)
ax.add_patch(S.plt.Rectangle((165, 2.75), 15, 0.5, color=S.TINT["model"], ec=S.ROLE["model"]))
S.label(ax, 172.5, 5.7, "band on the line: training, days 165 to 180", fs=9)
for d in (158, 170, 180, 190):
    S.label(ax, d, 0.35, f"day {d}", fs=9)
save(fig, 1, kind="diagram", data="story calendar (style sheet, Chapter 41 decisions); 04-code/ch41/output/drill_1.txt, drill_2.txt")
