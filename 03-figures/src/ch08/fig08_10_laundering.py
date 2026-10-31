"""Figure 8.10: the proposal that became a fact. One sentence, four documents, status rising with no evidence."""
from _common import S, plt, save, clean, STATUS_ROLE
fig, ax = S.figure(4.0); clean(ax, 10, 6.6)
steps = [("day -34\ndeal sheet", "V"), ("day 1\nkickoff deck", "P"), ("day 10\nstatus report", "R"),
         ("day 24\nscope v0.3", "F")]
for i, (t, s) in enumerate(steps):
    x = 0.1 + i * 2.5
    S.box(ax, x, 3.6, 2.1, 1.5, t, role=STATUS_ROLE[s], fs=10)
    S.label(ax, x + 1.05, 5.4, s, fs=11, ha="center", weight="bold")
    if i: S.arrow(ax, x - 0.4, 4.35, x, 4.35, weight="emphasis" if i > 1 else "control", color=S.ROLE["blocker"] if i > 1 else None)
S.label(ax, 2.6, 2.8, "no evidence event at either rise", fs=10)
S.box(ax, 2.6, 0.4, 7.2, 1.6, "day 26: Anne Kessler asked\nrewritten as decision OD-4", role="data", fs=10)
S.arrow(ax, 8.6, 3.6, 8.6, 2.0, weight="emphasis", color=S.ROLE["data"])
save(fig, 10, kind="diagram")
