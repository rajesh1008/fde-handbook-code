"""Figure 32.7: the 90-minute review: where the minutes went and what happened to the 41 answers."""
import re
from _common import S, save, text
t = text("review")
ag = re.findall(r"([a-z ]+?) (\d+)(?:,|$)", t.split("minutes): ")[1].splitlines()[0])
pre = int(re.search(r"pre-read: (\d+)", t).group(1)); fnd = int(re.search(r"\((\d+) findings", t).group(1))
clr = int(re.search(r"findings, (\d+) cleared", t).group(1))
fig, ax = S.figure(height=3.9)
roles = ["evidence", "data", "model", "blocker", "approval"]
left = 0
for (nm, m), r in zip(ag, roles):
    m = int(m); ax.barh(1, m, left=left, color=S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r], height=0.55)
    ax.text(left + m / 2, 1.36 + 0.2 * (roles.index(r) % 2), nm.strip(), ha="center", fontsize=9); ax.text(left + m / 2, 1, str(m), ha="center", va="center", fontsize=10, bbox=dict(fc="white", ec="none", pad=1))
    left += m
left = 0
for nm, v, r in (("accepted from pre-read", pre, "approval"), ("cleared", clr, "system"), ("findings", fnd, "blocker")):
    w = v * 90 / 41
    ax.barh(0, w, left=left, color=S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r], height=0.55)
    ax.text(left + w / 2, -0.42, nm, ha="center", fontsize=9); ax.text(left + w / 2, 0, str(v), ha="center", va="center", fontsize=10, bbox=dict(fc="white", ec="none", pad=1))
    left += w
ax.set_yticks([0, 1]); ax.set_yticklabels(["41 answers", "90 minutes"]); ax.set_ylim(-0.8, 1.85)
ax.set_xticks([]); ax.spines[["top", "right", "bottom"]].set_visible(False)
save(fig, 7, data="04-code/ch32/output/review.txt")
