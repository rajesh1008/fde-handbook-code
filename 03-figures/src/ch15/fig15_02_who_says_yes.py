"""Figure 15.2: five yeses stand between a request and one sample of Caldwell's claim files (days 9 to 48)."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4); blank(ax, (0, 10), (0, 7.2))
steps = [("Anne Kessler\nbusiness need, day 9", "approval"),
         ("privacy office\npurpose and readers", "approval"),
         ("claims operations\nextract, bank details redacted", "system"),
         ("archive delivered\n200 files, day 47", "data"),
         ("Priya Natarajan\nstorage and deletion, day 48", "approval")]
y = 6.2
for i, (t, role) in enumerate(steps):
    S.box(ax, 2.2, y - 0.5, 5.6, 1.0, t, role=role, fs=10)
    if i < len(steps) - 1:
        S.arrow(ax, 5.0, y - 0.5, 5.0, y - 0.9)
    y -= 1.4
S.label(ax, 8.1, 3.4, "38 days\nof review", fs=10, va="center")
S.arrow(ax, 8.0, 6.1, 8.0, 3.95, weight="data"); S.arrow(ax, 8.0, 2.85, 8.0, 1.5, weight="data")
save(fig, 2, kind="diagram", data="Chapter 3 (sample request, days 9 to 47); 04-code/ch15 histories (day 48)")
