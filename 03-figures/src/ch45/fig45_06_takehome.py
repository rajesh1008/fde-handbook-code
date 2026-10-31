"""Figure 45.6: the take-home against an agent-only baseline. The old one is cleared by an agent; the new one is not."""
from _common import S, save, text, nums
import re
b0 = float(re.search(r"baseline ([\d.]+)", text("takehome_v0")).group(1))
b1 = float(re.search(r"baseline ([\d.]+)", text("takehome_v1")).group(1))
w1 = float(re.search(r"candidate ([\d.]+)", text("takehome_v1")).group(1))
fig, ax = S.figure(height=4.2)
ax.bar([0, 1], [b0, b1], 0.5, color=[S.ROLE["blocker"], S.ROLE["approval"]], hatch=None)
ax.axhline(3.0, color=S.PAL["ink"], ls="--", lw=S.LW["control"])
ax.text(1.32, 3.06, "hire bar 3.0", fontsize=9.5)
ax.text(0, b0 + 0.08, f"{b0:.2f}", ha="center", fontsize=10.5); ax.text(1, b1 + 0.08, f"{b1:.2f}", ha="center", fontsize=10.5)
ax.set_xticks([0, 1]); ax.set_xticklabels(["v0: 8 hours,\nall agent-solvable", f"v1: 3-hour cap,\n{w1:.0%} needs the candidate"])
ax.set_ylabel("agent-only score (1 to 4)"); ax.set_ylim(0, 4.5); ax.set_xlim(-0.6, 1.9)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 6, data="04-code/ch45/output/takehome_v0.txt, takehome_v1.txt")
