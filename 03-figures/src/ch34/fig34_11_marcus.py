"""Figure 34.11: Greystone's gates waiting on each other, day 104 to the pilot on day 131."""
from _common import S, save, blank
fig, ax = S.figure(height=4.9); blank(ax, (0, 10), (0, 8))
b = [(0.1, 5.6, "day 104\nsecurity review\n12 findings", "evidence"), (2.6, 5.6, "day 108\nMarcus Bell's\nredline", "blocker"),
     (5.1, 5.6, "day 113\nengineering\nexhibit", "model"), (7.6, 5.6, "day 120\nF-10 closed", "approval"),
     (2.6, 1.4, "day 124\nExhibit A\nagreed", "approval"), (5.1, 1.4, "day 127\namendment\nsigned", "approval"),
     (7.6, 1.4, "day 131\npilot", "system")]
for x, y, t, r in b:
    S.box(ax, x, y, 2.2, 2.0, t, role=r, fs=9.5)
for (x1, y1), (x2, y2) in [((2.3, 6.6), (2.6, 6.6)), ((4.8, 6.6), (5.1, 6.6)), ((7.3, 6.6), (7.6, 6.6)),
                           ((6.2, 5.6), (3.7, 3.4)), ((8.7, 5.6), (6.2, 3.4)), ((4.8, 2.4), (5.1, 2.4)),
                           ((7.3, 2.4), (7.6, 2.4))]:
    S.arrow(ax, x1, y1, x2, y2)
save(fig, 11, kind="diagram", data="04-code/ch34/output/marcus.txt")
