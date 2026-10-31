"""Figure 17.8: who holds each key, day 57 template against day 63 module."""
from _common import S, save, blank
fig, ax = S.figure(height=4.2)
blank(ax, (0, 10), (0, 6.4))
S.label(ax, 0.1, 6.0, "day 57 template", fs=10, weight="bold"); S.label(ax, 5.6, 6.0, "day 63 module", fs=10, weight="bold")
rows = (("gateway key in repo\nNorthlight holds", "Caldwell secret\nrotates every 7 days"),
        ("tracing token\nNorthlight holds", "no tracing token\n(removed)"),
        ("bucket key\ncloud default", "Caldwell key\nin KMS"))
for i, (a, b) in enumerate(rows):
    y = 4.3 - i * 1.9
    S.box(ax, 0.1, y, 4.0, 1.35, a, role="blocker", ls="--")
    S.box(ax, 5.6, y, 4.3, 1.35, b, role="data")
    S.arrow(ax, 4.1, y + 0.67, 5.6, y + 0.67)
save(fig, 8, kind="diagram", data="04-code/ch17/output/keys.txt")
