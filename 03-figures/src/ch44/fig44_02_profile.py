"""Figure 44.2: the skill profile grid, people by competency, scored 0 to 3 from field evidence."""
from _common import S, save, text
import matplotlib.patches as P
L = text("profile").splitlines()
cols = L[0].split()[1:]
rows = [(" ".join(l.split()[:-8]), list(map(int, l.split()[-8:]))) for l in L[1:9]]
shade = {0: "#FFFFFF", 1: S.TINT["evidence"], 2: S.ROLE["evidence"], 3: S.ROLE["model"]}
fig, ax = S.figure(height=4.6)
for i, (p, v) in enumerate(rows):
    for j, s in enumerate(v):
        ax.add_patch(P.Rectangle((j, -i), 0.94, 0.9, fc=shade[s], ec=S.PAL["ink"], lw=0.5))
        ax.text(j + 0.47, -i + 0.45, str(s), ha="center", va="center", fontsize=9, color=S.text_on(shade[s]),
                bbox=dict(boxstyle="square,pad=0.1", fc=shade[s], ec="none"))
    ax.text(-0.15, -i + 0.45, p, ha="right", va="center", fontsize=9)
for j, c in enumerate(cols):
    ax.text(j + 0.47, 1.15, c, ha="center", fontsize=9)
ax.plot([-3.2, 8], [-5.15, -5.15], color=S.ROLE["blocker"], lw=S.LW["control"], ls="--")
ax.text(8.1, -5.6, "month-12\nhires", fontsize=9, va="center")
ax.set_xlim(-3.3, 9.3); ax.set_ylim(-7.3, 1.7); ax.axis("off")
save(fig, 2, data="04-code/ch44/output/profile.txt")
