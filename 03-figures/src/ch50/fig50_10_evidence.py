"""Figure 50.10: the same four questions answered at submission one and submission two."""
from _common import S, save, text, blank
s1, s2 = text("committee_s1"), text("committee_s2")
assert "evidenced 53" in s1 and "evidenced 75" in s2
rows = [("plan items", ("53 of 75", "blocker"), ("75 of 75", "approval")),
        ("outcomes", ("vendor scored, 200", "blocker"), ("bank scored, 600", "approval")),
        ("metrics", ("vendor computes", "blocker"), ("bank computes", "approval")),
        ("provider change", ("no control", "blocker"), ("pinned, notice, fallback", "approval"))]
fig, ax = S.figure(height=3.9); blank(ax, (0, 10), (0, 5.4))
S.label(ax, 3.7, 5.0, "day 118", fs=10, ha="center", weight="bold"); S.label(ax, 7.7, 5.0, "day 152", fs=10, ha="center", weight="bold")
for i, (n, a, b) in enumerate(rows):
    y = 3.9 - i * 1.15
    S.label(ax, 0.0, y + 0.4, n, fs=9.5, va="center")
    S.box(ax, 2.1, y, 3.2, 0.8, a[0], role=a[1], fs=9.5); S.box(ax, 6.1, y, 3.2, 0.8, b[0], role=b[1], fs=9.5)
    S.arrow(ax, 5.35, y + 0.4, 6.05, y + 0.4, weight="data")
save(fig, 10, kind="diagram", data="04-code/ch50/output/committee_s1.txt, committee_s2.txt")
