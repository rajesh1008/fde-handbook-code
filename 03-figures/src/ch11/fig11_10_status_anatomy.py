"""Figure 11.10: the seven parts of the weekly status, in reading order, with what each must carry."""
from _common import S, save, blank
fig, ax = S.figure(4.6); blank(ax, ylim=(0, 7.4))
parts = [("headline", "slip, cause, date", "cost"), ("done", "acceptance only", "system"),
         ("in progress", "", "system"), ("blockers", "owner, age, date", "blocker"), ("risks", "trigger", "data"),
         ("decisions needed", "owner, date", "approval"), ("next week", "", "evidence")]
for i, (p, note, r) in enumerate(parts):
    y = 6.5 - i * 0.98
    S.box(ax, 0.3, y, 3.6, 0.78, p, role=r, fs=10, lw=S.LW["emphasis"] if i == 0 else None)
    if note:
        S.label(ax, 4.2, y + 0.39, note, fs=10, va="center")
S.box(ax, 7.3, 6.5, 2.5, 0.78, "computed color", role="evidence", fs=10)
S.box(ax, 7.3, 5.52, 2.5, 0.78, "gates line", role="approval", fs=10)
S.arrow(ax, 7.3, 6.89, 6.4, 6.89, weight="data"); S.arrow(ax, 7.3, 5.91, 6.4, 6.7, weight="data")
save(fig, 10, kind="diagram")
