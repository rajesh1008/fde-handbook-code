"""Figure 18.9: three things Northlight did not bring, and what it used instead at Caldwell."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6))
rows = [("hosting platform", "Caldwell's container\nservice, team account"), ("model gateway", "Caldwell's gateway,\nthrough the adapter"),
        ("audit store", "Caldwell's audit store;\nNorthlight keeps a copy-free index")]
for i, (no, yes) in enumerate(rows):
    y = 4.3 - i * 1.7
    S.box(ax, 0.2, y, 3.2, 1.2, f"no new {no}", role="blocker", fs=10, ls="--")
    S.arrow(ax, 3.4, y + 0.6, 4.4, y + 0.6)
    S.box(ax, 4.4, y, 5.4, 1.2, yes, role="system", fs=10)
save(fig, 9, kind="diagram", data="chapter text (Section 18.5)")
