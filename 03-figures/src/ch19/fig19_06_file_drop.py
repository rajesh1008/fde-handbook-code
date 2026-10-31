"""Figure 19.4: the checks a nightly file passes before a single row is loaded."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 12), (0, 6))
steps = ["arrived by\ndeadline", "new bytes", "header\nmatches", "volume\nin band", "load"]
for i, t in enumerate(steps):
    x = 0.2 + i * 2.4
    S.box(ax, x, 3.4, 1.9, 1.4, t, role="system" if i < 4 else "approval", fs=10)
    if i < 4:
        S.arrow(ax, x + 1.9, 4.1, x + 2.4, 4.1)
        S.arrow(ax, x + 0.95, 3.4, x + 0.95, 2.1, ls="--", weight="data")
for i, t in enumerate(["alarm", "skip", "refuse", "refuse"]):
    S.box(ax, 0.35 + i * 2.4, 1.0, 1.6, 1.1, t, role="blocker", fs=10)
save(fig, 6, kind="diagram", data="fieldkit.connectors.FileDrop")
