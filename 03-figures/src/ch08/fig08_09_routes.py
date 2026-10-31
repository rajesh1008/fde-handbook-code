"""Figure 8.9: every excluded item has a route; nothing excluded is left without a destination."""
from _common import S, plt, save, clean
fig, ax = S.figure(4.4); clean(ax, 10, 7)
rows = [("attorney letters", "legal mail coordinator"), ("finance-cage mail", "finance cage"),
        ("administrator files", "nightly import"), ("medical records", "claim, unread"),
        ("police, fire reports", "claim, unread"), ("photos, other mail", "claim or adjuster inbox")]
for i, (a, b) in enumerate(rows):
    y = 6.0 - i * 1.1
    S.box(ax, 0.2, y, 3.4, 0.75, a, role="evidence", fs=10)
    S.arrow(ax, 3.7, y + 0.37, 5.8, y + 0.37)
    S.box(ax, 5.9, y, 3.9, 0.75, b, role="system", fs=10)
S.label(ax, 3.9, 6.95, "OD-6 may bring one in", fs=9)
save(fig, 9, kind="diagram")
