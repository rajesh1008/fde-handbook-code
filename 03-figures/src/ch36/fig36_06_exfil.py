"""Figure 36.6: output channels that leaked on suite v2 and on v3, with the measured count."""
from _common import S, save, text
from matplotlib.patches import Rectangle
rows = []
for l in text("exfil").splitlines()[2:-1]:
    rows.append((l[:15].strip(), int(l.split()[-2]), int(l.split()[-1])))
assert len(rows) == 7 and all(b == 0 for *_, b in rows)
fig, ax = S.figure(height=4.2)
for i, (ch, a, b) in enumerate(rows[::-1]):
    for j, v in enumerate((a, b)):
        r = "blocker" if v else "approval"
        ax.add_patch(Rectangle((j * 1.2, i), 1.0, 0.8, facecolor=S.TINT[r], edgecolor=S.ROLE[r], lw=1.2,
                               hatch=S.HATCH[r]))
        ax.text(j * 1.2 + 0.5, i + 0.4, str(v), ha="center", va="center", fontsize=10,
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))
ax.set_yticks([i + 0.4 for i in range(7)]); ax.set_yticklabels([r[0] for r in rows[::-1]])
ax.set_xticks([0.5, 1.7]); ax.set_xticklabels(["v2, day 124", "v3, day 128"])
ax.set_xlim(-0.1, 2.3); ax.set_ylim(-0.2, 7.0)
ax.tick_params(length=0); ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
save(fig, 6, data="04-code/ch36/output/exfil.txt")
