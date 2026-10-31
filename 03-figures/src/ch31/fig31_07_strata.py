"""Figure 31.7: gold-heldout accuracy by stratum, p7 (day 94) against rc-1 (day 156) (scorecard.txt)."""
from _common import S, save, text, nums
rows = [l for l in text("scorecard").splitlines() if l[:1].islower() and "%" in l and l.split()[0] in
        ("first", "police", "repair", "medical", "adjuster", "photo")]
names = [l[:22].strip() for l in rows]; v = [nums(l[22:]) for l in rows]
fig, ax = S.figure(height=4.2)
for i, r in enumerate(v):
    a, b = r[1], r[2]
    ax.plot([a, b], [i, i], color=S.PAL["light"], lw=4)
    ax.scatter([a], [i], color=S.ROLE["evidence"], marker="s", s=40, zorder=3)
    ax.scatter([b], [i], color=S.ROLE["system"], marker="o", s=50, zorder=3)
    S.label(ax, b + 0.8, i, f"{b:.1f}", fs=9, va="center")
ax.set_yticks(range(len(names)), names, fontsize=9); ax.set_ylim(7.5, -1.3); ax.set_xlim(55, 102)
ax.set_xlabel("fields right (%), Lena Ortiz labels")
S.label(ax, 56, -0.95, "square: p7, day 94   circle: rc-1, day 156", fs=9)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 7, data="04-code/ch31/output/scorecard.txt")
