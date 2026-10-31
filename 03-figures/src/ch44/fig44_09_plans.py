"""Figure 44.9: needs met, needs held by one person, and coordination hours for the three staffing plans."""
from _common import S, save, text
import re, numpy as np
L = [l for l in text("pods").splitlines() if "needs met" in l]
vals = [list(map(int, re.findall(r"needs met (\d+) of (\d+); met by a single person (\d+); coordination (\d+)", l)[0])) for l in L]
labels = ["solo", "pods", "pods + shared\nevaluation lead"]
fig, (a1, a2) = S.figure(height=3.9, ncols=2)
x = np.arange(3)
a1.bar(x - 0.2, [v[0] for v in vals], 0.38, color=S.ROLE["approval"], ec="white", label="needs met (of 14)")
a1.bar(x + 0.2, [v[2] for v in vals], 0.38, color=S.ROLE["blocker"], hatch=S.HATCH["blocker"], ec="white", label="met by one person")
a1.set_xticks(x); a1.set_xticklabels(labels, fontsize=9); a1.set_ylim(0, 18); a1.legend(fontsize=9, loc="upper left")
a2.bar(x, [v[3] for v in vals], 0.5, color=S.ROLE["cost"], hatch=S.HATCH["cost"], ec="white")
for i, v in enumerate(vals):
    a2.text(i, v[3] + 0.6, f"{v[3]} h", ha="center", fontsize=9)
a2.set_xticks(x); a2.set_xticklabels(labels, fontsize=9); a2.set_ylabel("coordination, hours a week"); a2.set_ylim(0, 33)
for a in (a1, a2):
    a.spines[["top", "right"]].set_visible(False)
save(fig, 9, data="04-code/ch44/output/pods.txt")
