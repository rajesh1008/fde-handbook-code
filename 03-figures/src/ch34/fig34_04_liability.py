"""Figure 34.4: liability follows the action. Release level of each action, and what the signed clause says."""
from _common import S, save, blank
fig, ax = S.figure(height=4.9); blank(ax, (0, 10), (0, 8))
rows = [("read and draft", "a person decides\non the draft", "cap: 12 months\nof fees", "evidence"),
        ("write,\ncompensated", "release boundary\nand undo path", "cap; undo path\nis evidence", "system"),
        ("refused", "never offered\nby the system", "never\nindemnified", "blocker")]
for i, (lvl, who, cl, r) in enumerate(rows):
    y = 5.6 - i * 2.4
    S.box(ax, 0.1, y, 2.6, 1.7, lvl, role=r, fs=10)
    S.box(ax, 3.4, y, 3.0, 1.7, who, role="model", fs=9.5)
    S.box(ax, 7.1, y, 2.8, 1.7, cl, role="approval" if r != "blocker" else "blocker", fs=9.5)
    S.arrow(ax, 2.7, y + 0.85, 3.4, y + 0.85); S.arrow(ax, 6.4, y + 0.85, 7.1, y + 0.85)
save(fig, 4, kind="diagram", data="04-code/ch34/output/liability.txt")
