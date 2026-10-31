"""Figure 9.15: the single-experience principle at Caldwell: one entry point, many components behind it."""
from _common import S, save, blank
fig, ax = S.figure(4.2); blank(ax, (0, 10), (0, 6.4))
S.box(ax, 0.2, 2.6, 2.4, 1.2, "adjuster's\nclaim queue", role="evidence", fs=10.5)
items = [("7 code services", "system"), ("2 rule sets", "approval"), ("2 classifiers", "data"), ("1 cited summary", "model")]
for i, (t, r) in enumerate(items):
    y = 5.0 - i * 1.45
    S.box(ax, 6.2, y, 3.4, 1.0, t, role=r, fs=10)
    S.arrow(ax, 6.2, y + 0.5, 2.6, 3.2, weight="data")
S.label(ax, 3.2, 5.7, "one place to work", fs=10, weight="bold")
S.label(ax, 3.2, 0.5, "one trace per document", fs=10, weight="bold")
save(fig, 15, kind="diagram")
