"""Figure 40.12: the monitors run in Caldwell's account under Caldwell's identity; Northlight reads, never writes."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4); blank(ax, (0, 10), (0, 8))
S.box(ax, 0.1, 0.4, 6.8, 7.2, "", role="approval", fs=10)
S.label(ax, 0.4, 6.9, "Caldwell account", fs=10.5, weight="bold")
S.box(ax, 0.6, 4.2, 2.8, 1.8, "run records", role="data", fs=10)
S.box(ax, 3.7, 4.2, 2.8, 1.8, "cw-mrm-monitor", role="system", fs=10)
S.box(ax, 0.6, 1.0, 2.8, 1.8, "M1 to M6", role="evidence", fs=10)
S.box(ax, 3.7, 1.0, 2.8, 1.8, "P1 to P3", role="evidence", fs=10)
S.arrow(ax, 3.4, 5.1, 3.7, 5.1); S.arrow(ax, 5.1, 4.2, 2.0, 2.8); S.arrow(ax, 5.1, 4.2, 5.1, 2.8)
S.box(ax, 7.4, 3.3, 2.5, 1.8, "Northlight", role="model", fs=10)
S.arrow(ax, 7.4, 4.2, 6.5, 2.0, ls="--", color=S.PAL["grey"])
S.label(ax, 7.3, 2.2, "read only", fs=9.5)
save(fig, 12, kind="diagram", data="04-code/ch40/output/monitor.txt (monitor list)")
