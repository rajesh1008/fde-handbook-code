"""Figure 44.1: the FDE function's headcount by month, with joins and departures."""
from _common import S, save, text
rows = [l.split() for l in text("headcount").splitlines()[1:13]]
m = [int(r[0]) for r in rows]; n = [int(r[1]) for r in rows]
fig, ax = S.figure(height=3.9)
ax.step(m, n, where="mid", color=S.ROLE["model"], lw=S.LW["emphasis"])
ax.fill_between(m, n, step="mid", color=S.TINT["model"])
notes = [(4, "+2 via old loop", "system", (2.6, 6.0)), (7, "+1 via old loop", "system", (5.6, 7.0)),
         (9, "one moves to platform", "blocker", (7.6, 2.6)), (11, "one goes independent", "blocker", (9.6, 1.6)),
         (12, "+2 via new exercise", "approval", (9.6, 7.0))]
for mm, t, r, xy in notes:
    y = n[mm - 1]
    ax.annotate(t, (mm - 0.5, y), xy, fontsize=9, color=S.PAL["ink"],
                arrowprops=dict(arrowstyle="-", color=S.ROLE[r], lw=1.5))
ax.set_xticks(range(1, 13)); ax.set_xlabel("function month"); ax.set_ylabel("FDEs on the function")
ax.set_ylim(0, 7.6); ax.set_xlim(0.5, 12.7); ax.spines[["top", "right"]].set_visible(False)
save(fig, 1, data="04-code/ch44/output/headcount.txt")
