"""Figure 32.13: declared flows reconciled with observed flows."""
import re
from _common import S, save, text, blank
t = text("dataflows")
dec = int(re.search(r"declared flows: (\d+)", t).group(1)); obs = int(re.search(r"day 102: (\d+) pairs", t).group(1))
m, u, n = map(int, re.search(r"matched (\d+); undeclared (\d+); declared but not seen (\d+)", t).groups())
fig, ax = S.figure(height=4.0); blank(ax, (0, 10), (0, 6))
S.box(ax, 0.2, 3.8, 2.6, 1.3, f"declared\n{dec}", role="evidence"); S.box(ax, 0.2, 0.9, 2.6, 1.3, f"observed\n{obs}", role="system")
S.box(ax, 3.9, 2.35, 2.2, 1.3, f"matched\n{m}", role="approval")
S.box(ax, 7.2, 3.8, 2.6, 1.3, f"not seen {n}\nSIEM export", role="data")
S.box(ax, 7.2, 0.9, 2.6, 1.3, f"undeclared {u}\nfinding F-08", role="blocker", lw=S.LW["emphasis"])
S.arrow(ax, 2.8, 4.4, 3.9, 3.2); S.arrow(ax, 2.8, 1.5, 3.9, 2.8)
S.arrow(ax, 2.8, 4.7, 7.2, 4.6); S.arrow(ax, 2.8, 1.2, 7.2, 1.4, color=S.ROLE["blocker"], weight="emphasis")
save(fig, 13, kind="diagram", data="04-code/ch32/output/dataflows.txt")
