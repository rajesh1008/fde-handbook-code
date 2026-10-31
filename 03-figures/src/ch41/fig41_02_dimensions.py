"""Figure 41.2: readiness credit by dimension for Caldwell day 176, Caldwell day 183 and Pennant; the naive score is 1.0 for all three."""
from _common import S, save, text
import numpy as np
def dims(name):
    l = [x for x in text(name).splitlines() if x.startswith("by dimension:")][0].split(":")[1].split()
    return dict(zip(l[0::2], map(float, l[1::2])))
sets = [("Caldwell day 176", dims("readiness_caldwell-before"), "blocker"),
        ("Caldwell day 183", dims("readiness_caldwell-after"), "approval"),
        ("Pennant", dims("readiness_pennant"), "data")]
names = list(sets[0][1])
fig, ax = S.figure(height=4.4)
x = np.arange(len(names))
for k, (lab, d, r) in enumerate(sets):
    ax.bar(x + (k - 1) * 0.27, [d[n] for n in names], 0.25, color=S.ROLE[r], hatch=S.HATCH[r], ec="white", label=lab)
ax.axhline(1.0, color=S.PAL["ink"], lw=0.75, ls="--"); ax.text(-0.45, 1.03, "naive score: every artifact exists", fontsize=9)
ax.set_xticks(x); ax.set_xticklabels(names); ax.set_ylim(0, 1.32); ax.set_ylabel("evidence credit")
ax.legend(loc="upper right", fontsize=9, ncol=3); ax.spines[["top", "right"]].set_visible(False)
save(fig, 2, data="04-code/ch41/output/readiness_*.txt")
