"""Figure 4.2: what survives for the auditor. The deployment's chain per output against what a demo leaves."""
from _common import S, save, title, blank

fig, ax = blank(5.0)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
S.label(ax, 2.6, 9.45, "a deployment keeps", fs=11, ha="center", weight="bold")
S.label(ax, 7.6, 9.45, "a demo leaves", fs=11, ha="center", weight="bold")
chain = [("source page", "data"), ("extracted field", "model"), ("prompt, model,\ncode versions", "system"),
         ("reviewer correction", "evidence"), ("customer-owned\ngateway log", "system"), ("evidence pack", "approval")]
h, gap = 1.05, 0.42
for i, (t, r) in enumerate(chain):
    y = 8.55 - (i + 1) * h - i * gap
    S.box(ax, 0.9, y, 3.4, h, t, role=r, fs=10)
    if i:
        S.arrow(ax, 2.6, y + h + gap, 2.6, y + h)
demo = ["screen recording", "slide saying 98%", "vendor's own log", "salesperson's\nmemory"]
for i, t in enumerate(demo):
    y = 8.55 - (i + 1) * 1.35 - i * 0.55
    S.box(ax, 5.9, y, 3.4, 1.35, t, role="blocker", fs=10)
S.label(ax, 7.6, 0.55, "no link to any output", fs=10, ha="center")
title(ax, "Only the chain can answer an audit question about one claim")
save(fig, 2, kind="diagram", data="none (concept diagram; Section 4.2 lists the chain)")
