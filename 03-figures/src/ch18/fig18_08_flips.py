"""Figure 18.8: the alias move on day 77, item by item on the 200-item gold set."""
import re
from _common import S, save, text
fig, ax = S.figure(height=3.9)
t = text("version_drift")
m = re.search(r"both correct (\d+), gained (\d+), lost (\d+), both wrong (\d+)", t)
labels = ["both correct", "gained", "lost", "both wrong"]
vals = [int(v) for v in m.groups()]
roles = ["evidence", "approval", "blocker", "cost"]
ax.bar(range(4), vals, color=[S.ROLE[r] for r in roles], edgecolor=S.PAL["ink"], lw=S.LW["data"])
for i, v in enumerate(vals):
    ax.text(i, v + 3, str(v), ha="center", fontsize=10)
agg = re.search(r"old version (\d+) correct \(([\d.]+)%\), new version (\d+) \(([\d.]+)%\)", t)
ax.text(1.5, 120, f"aggregate: {agg.group(2)}% to {agg.group(4)}%\nthe {vals[2]} lost items are the review", ha="center", fontsize=10)
ax.set_xticks(range(4)); ax.set_xticklabels(labels); ax.set_ylabel("gold-set items"); ax.set_ylim(0, 195)
save(fig, 8, data="04-code/ch18/output/version_drift.txt")
