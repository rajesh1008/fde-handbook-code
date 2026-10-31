"""Figure 10.3: Pennant's 41 layouts in five kinds: hours per layout from the timed spike (low to high, most likely
marked) and the kind's total."""
from _common import S, plt, save, quiet
with quiet():
    from inventories import PENNANT_KINDS
fig, ax = S.figure(3.8)
for y, (kind, n, lo, li, hi) in enumerate(PENNANT_KINDS):
    ax.plot([lo, hi], [y, y], color=S.ROLE["data"], lw=6, solid_capstyle="butt")
    ax.plot([li], [y], marker="D", color=S.PAL["ink"], markersize=6)
    ax.text(hi + 1.5, y, f"{n} layouts, {n * li} h", va="center", fontsize=9)
ax.set_yticks(range(len(PENNANT_KINDS))); ax.set_yticklabels([k[0] for k in PENNANT_KINDS], fontsize=9.5)
ax.axvline(25, color=S.PAL["grey"], lw=S.LW["data"], ls="--"); ax.text(25.8, -0.62, "25 h per layout (Chapter 2)", fontsize=9)
ax.set_xlabel("hours per layout (low to high; diamond: most likely)"); ax.set_xlim(0, 85); ax.set_ylim(4.5, -0.9)
save(fig, 3)
