"""Figure 44.4: the four hiring exercises and the competencies each one observes, with floors marked."""
from _common import S, save, blank
import world as W
fig, ax = S.figure(height=4.6); blank(ax, (0, 10), (0, 8.6))
ex = list(W.EXERCISES.items())
short = ["E1 discovery role-play", "E2 classify the workflow", "E3 paired build", "E4 sponsor note"]
ys = [7.0, 5.0, 3.0, 1.0]
cy = {c: 8.0 - i * 1.0 for i, c in enumerate(W.COMPETENCIES)}
for (k, cs), y, s in zip(ex, ys, short):
    S.box(ax, 0.2, y - 0.4, 3.4, 0.8, s, role="system", fs=9)
    for c in cs:
        S.arrow(ax, 3.6, y, 6.0, cy[c] - 0.15, weight="data", color=S.ROLE["evidence"])
for c, y in cy.items():
    floor = c in W.FLOORS
    S.box(ax, 6.0, y - 0.45, 2.4, 0.6, c, role="blocker" if floor else "evidence", fs=9)
    if floor:
        S.label(ax, 9.25, y - 0.15, "floor 2", fs=9)
save(fig, 4, kind="diagram", data="04-code/ch44/world.py EXERCISES, FLOORS")
