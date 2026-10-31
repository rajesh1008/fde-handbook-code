"""Figure 42.4: the page route as handed over and after the day-43 runbook change (ownership.py lint)."""
from _common import S, save, blank
fig, ax = S.figure(height=4.6); blank(ax, (0, 10), (0, 6.6))
ax.text(0.2, 6.2, "as handed over", fontsize=10, weight="bold"); ax.text(0.2, 2.9, "after day 43", fontsize=10, weight="bold")
for y, steps in ((4.2, [("alert", "system"), ("vendor\non-call", "blocker"), ("FDE", "evidence"), ("Jenna\nby name", "blocker")]),
                 (0.9, [("alert", "system"), ("Pennant\non-call", "approval"), ("deputy", "approval"), ("operations\nrole", "approval")])):
    for i, (t, r) in enumerate(steps):
        S.box(ax, 0.2 + i * 2.5, y, 2.0, 1.5, t, role=r, fs=10)
        if i:
            S.arrow(ax, 0.2 + i * 2.5 - 0.5, y + 0.75, 0.2 + i * 2.5, y + 0.75)
save(fig, 4, kind="diagram", data="04-code/ch42/output/ownership.txt (page route lint)")
