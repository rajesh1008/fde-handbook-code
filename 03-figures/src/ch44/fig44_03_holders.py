"""Figure 44.3: people at level 3 per competency in months 7, 11 and 12."""
from _common import S, save, text
import numpy as np
L = [l for l in text("profile").splitlines() if "level-3 holders" in l]
def parse(l):
    parts = l.split(": ")[-1].split(", ")
    return [p.split()[0] for p in parts], [int(p.split()[1]) for p in parts]
names, _ = parse(L[0])
sets = [("month 7, six people", parse(L[0])[1], "model"), ("month 11, four people", parse(L[1])[1], "blocker"),
        ("month 12, six people", parse(L[2])[1], "approval")]
fig, ax = S.figure(height=4.0)
x = np.arange(len(names))
for k, (lab, v, r) in enumerate(sets):
    ax.bar(x + (k - 1) * 0.27, v, 0.25, color=S.ROLE[r], hatch=S.HATCH[r], ec="white", label=lab)
ax.axhline(1, color=S.PAL["ink"], lw=0.75, ls="--"); ax.text(7.45, 0.82, "one\nholder", fontsize=9, ha="left")
ax.set_xticks(x); ax.set_xticklabels(names); ax.set_ylabel("people at level 3"); ax.set_ylim(0, 4.7); ax.set_xlim(-0.5, 8.2)
ax.legend(loc="upper center", fontsize=9, ncol=3); ax.spines[["top", "right"]].set_visible(False)
save(fig, 3, data="04-code/ch44/output/profile.txt")
