"""Figure 44.6: pairwise rater agreement on the discovery role-play before and after behavioral anchors."""
from _common import S, save, text
import numpy as np
L = text("calibrate").splitlines()
def block(start):
    i = [k for k, l in enumerate(L) if l.startswith(start)][0]
    return [(l.split()[1], float(l.split()[2])) for l in L[i + 1:i + 4]]
b, a = block("before"), block("after")
fig, ax = S.figure(height=3.9)
x = np.arange(3)
ax.bar(x - 0.2, [v for _k, v in b], 0.38, color=S.ROLE["blocker"], hatch=S.HATCH["blocker"], ec="white", label="before anchors, month 8")
ax.bar(x + 0.2, [v for _k, v in a], 0.38, color=S.ROLE["approval"], ec="white", label="after anchors, month 10")
ax.axhline(0, color=S.PAL["ink"], lw=0.75); ax.axhline(0.6, color=S.PAL["ink"], lw=0.75, ls="--")
ax.text(2.6, 0.63, "target 0.60", fontsize=9, ha="right")
ax.set_xticks(x); ax.set_xticklabels([k for k, _v in b]); ax.set_ylabel("Cohen's kappa"); ax.set_ylim(-0.45, 1.05)
ax.legend(loc="upper left", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 6, data="04-code/ch44/output/calibrate.txt")
