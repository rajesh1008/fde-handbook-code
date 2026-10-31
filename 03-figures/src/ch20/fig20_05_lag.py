"""Figure 20.5: days after first release before each region offered extract-2026-04 (stand-in catalog)."""
import re
from _common import S, save, text
t = text("region_drift")
rows = re.findall(r"^(aws|azure|gcp)\s+(\S+)\s+(not offered|offered from day (\d+))", t, re.M)
now = int(re.search(r"offered, (\d+) days after", t).group(1))
fig, ax = S.figure(height=4.0)
names = {"aws": "AWS", "azure": "Azure", "gcp": "Google"}
labels = [f"{names[c]} {r}" for c, r, _, _ in rows]
vals = [int(d) if d else now for _, _, _, d in rows]
cols = [S.ROLE["blocker"] if not d else S.ROLE["evidence"] for _, _, _, d in rows]
ax.barh(range(len(rows)), vals, color=cols, edgecolor=S.PAL["ink"], lw=S.LW["data"])
for i, (_, _, s, d) in enumerate(rows):
    ax.text(vals[i] + 1, i, f"day {d}" if d else "not offered yet", va="center", fontsize=10)
ax.set_yticks(range(len(rows))); ax.set_yticklabels(labels); ax.invert_yaxis()
ax.set_xlim(0, now + 22); ax.set_xlabel("days after first release")
save(fig, 5, data="04-code/ch20/output/region_drift.txt (stand-in catalog)")
