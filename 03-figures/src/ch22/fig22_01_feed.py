"""Figure 22.1: the feed, from three channels through the door, the pipeline and the rules to matched or a named queue."""
import re
from _common import S, save, blank, text
w = text("week_v1")
ch = dict(re.findall(r"(edi|scan|photo) (\d+)", w.splitlines()[2]))
m = re.search(r"matched as scored by the reconciliation team: (\d+)", w).group(1)
fig, ax = S.figure(height=4.4)
blank(ax, (0, 10), (0, 6))
for i, (k, role) in enumerate([("edi", "system"), ("scan", "data"), ("photo", "blocker")]):
    S.box(ax, 0.1, 4.3 - i * 1.5, 1.7, 1.0, f"{k}\n{int(ch[k]):,}", role=role, fs=10)
    S.arrow(ax, 1.8, 4.8 - i * 1.5, 2.5, 3.2, weight="data")
S.box(ax, 2.5, 2.6, 1.6, 1.2, "door\nqs-1.0", role="evidence", fs=10, lw=S.LW["emphasis"])
S.arrow(ax, 4.1, 3.2, 4.6, 3.2, weight="data")
S.box(ax, 4.6, 2.6, 1.8, 1.2, "read, classify,\nlink", role="model", fs=10)
S.arrow(ax, 6.4, 3.2, 6.9, 3.2, weight="data")
S.box(ax, 6.9, 2.6, 1.3, 1.2, "rules\nR1-R6", role="evidence", fs=10)
S.arrow(ax, 8.2, 3.6, 8.6, 4.5, weight="data")
S.box(ax, 8.6, 4.2, 1.4, 1.0, f"matched\n{int(m):,}", role="approval", fs=10)
S.arrow(ax, 8.2, 2.8, 8.6, 1.6, weight="data")
S.box(ax, 8.6, 0.9, 1.4, 1.2, "four\nqueues", role="blocker", fs=10)
S.arrow(ax, 3.3, 2.6, 8.6, 1.3, weight="control", ls="--")
S.label(ax, 2.5, 0.4, "held at the door goes back to the sender", fs=9, color=S.PAL["slate"])
save(fig, 1, kind="diagram", data="04-code/ch22/output/week_v1.txt")
