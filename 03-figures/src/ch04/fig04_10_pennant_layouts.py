"""Figure 4.10: Pennant's layout inventory by kind, the one layout the demo matched, and the rest."""
from _common import S, save, title
import matplotlib.pyplot as plt
from tryit import PENNANT_LAYOUTS, PENNANT_COVERED

kinds = sorted(PENNANT_LAYOUTS, key=lambda k: PENNANT_LAYOUTS[k])
fig, ax = plt.subplots(figsize=(S.WIDTH_IN, 3.9))
for i, k in enumerate(kinds):
    n = PENNANT_LAYOUTS[k]; cov = n if k in PENNANT_COVERED else 0
    if cov:
        ax.barh(i, cov, color=S.ROLE["approval"], edgecolor=S.PAL["ink"], lw=0.75, height=0.6)
    if n - cov:
        ax.barh(i, n - cov, left=cov, color=S.TINT["blocker"], hatch=S.HATCH["blocker"], edgecolor=S.ROLE["blocker"],
                lw=0.75, height=0.6)
    ax.text(n + 0.5, i, f"{n}" + "", va="center", fontsize=9)
ax.set_yticks(range(len(kinds)), kinds, fontsize=9)
ax.set_xlim(0, 36); ax.set_xlabel("layouts")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=S.ROLE["approval"], edgecolor=S.PAL["ink"], label="matched by the sales demo"),
                   Patch(facecolor=S.TINT["blocker"], hatch=S.HATCH["blocker"], edgecolor=S.ROLE["blocker"],
                         label="uncovered: route to the exceptions team")],
          frameon=False, fontsize=9, loc="center right")
title(ax, "One layout of 41")
save(fig, 10, data="04-code/ch04/tryit.py PENNANT_LAYOUTS (Pennant layout inventory v1)")
