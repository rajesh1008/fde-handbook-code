"""Figure 21.11: reconstructing one number for an examiner, step by step, without and with the lineage chain."""
import sys
from _common import S, save, R
sys.path.insert(0, str(R / "04-code/ch21"))
from reconstruct import WITHOUT, WITH
fig, ax = S.figure(height=3.9)
for y, steps in ((1, WITHOUT), (0, WITH)):
    left = 0
    for i, (name, sysname, m, ok) in enumerate(steps):
        ax.barh(y, m, left=left, height=0.45, color=(S.ROLE["system"] if i % 2 == 0 else S.PAL["slate"]) if ok else S.ROLE["blocker"],
                edgecolor="white")
        left += m
    ax.text(left + 3, y, f"{left:.0f} min", va="center", fontsize=11, weight="bold", color=S.PAL["ink"])
ax.text(150, 1.36, "FX rate on day 66: unrecoverable", fontsize=10, color=S.PAL["ink"])
ax.set_yticks([1, 0], ["without\nlineage", "with\nlineage"]); ax.set_xlim(0, 290); ax.set_ylim(-0.5, 1.6)
ax.set_xlabel("minutes (assumed per-step times; 7 steps against 3)")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 11, data="04-code/ch21/reconstruct.py WITHOUT, WITH; output/reconstruct.txt")
