"""Figure 17.9: every place a log line from the runner can land."""
from _common import S, save, blank
fig, ax = S.figure(height=4.3)
blank(ax, (0, 10), (0, 6.5))
S.box(ax, 3.9, 2.7, 2.2, 1.1, "runner", role="system", lw=S.LW["emphasis"])
keep = ("runner log\ngroup", "egress\nlog", "recheck\nlog")
for i, lab in enumerate(keep):
    x = 0.2 + i * 3.3
    S.box(ax, x, 4.9, 2.8, 1.2, lab, role="evidence"); S.arrow(ax, 5.0, 3.8, x + 1.4, 4.9, weight="data")
gone = ("vendor tracing", "provider request log", "laptop notebook")
for i, lab in enumerate(gone):
    x = 0.2 + i * 3.3
    S.box(ax, x, 0.3, 2.8, 1.1, lab, role="blocker", ls="--", fs=9.5)
S.label(ax, 0.2, 1.75, "removed: copies Caldwell cannot read or delete", fs=10, color=S.PAL["ink"])
S.label(ax, 6.3, 3.15, "Caldwell's archive,\nCaldwell's key", fs=9.5)
save(fig, 10, kind="diagram", data="04-code/ch17/output/env_doc.txt; chapter text")
