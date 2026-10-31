"""Figure 20.6: the same suite, three answers, by region and served version (Pennant)."""
import re
from _common import S, save, text
t = text("region_drift")
us = float(re.search(r"extract-2026-04: ([\d.]+)% on the US-lane", t).group(1))
naive = float(re.search(r"field accuracy ([\d.]+)% on 120 EU-lane", t).group(1))
hyp = float(re.search(r"would score ([\d.]+)%", t).group(1))
fig, ax = S.figure(height=3.9)
labels = ["US lanes, us-central1\nserved 2026-04", "EU lanes, europe-west4\nserved 2026-01 (latest)", "EU lanes on 2026-04\n(stand-in only)"]
vals = [us, naive, hyp]
cols = [S.ROLE["approval"], S.ROLE["blocker"], S.TINT["evidence"]]
ax.barh(range(3), vals, color=cols, edgecolor=S.PAL["ink"], lw=S.LW["data"], hatch=[None, None, "xx"])
for i, v in enumerate(vals):
    ax.text(v + 0.2, i, f"{v:.1f}%", va="center", fontsize=10)
ax.axvline(85, color=S.PAL["ink"], lw=S.LW["control"], ls="--")
ax.text(85.15, -0.55, "pass line 85%", fontsize=10)
ax.set_yticks(range(3)); ax.set_yticklabels(labels)
ax.set_xlim(80, 94); ax.set_ylim(2.5, -0.8); ax.set_xlabel("field accuracy, %")
save(fig, 6, data="04-code/ch20/output/region_drift.txt")
