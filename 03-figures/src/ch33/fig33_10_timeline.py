"""Figure 33.10: Caldwell's model-risk review from day 71 to day 153."""
import re
from _common import S, save, text
t = text("review")
ev = [(int(d), s) for d, s in re.findall(r"^  day +(\d+)  (.*)$", t, re.M)]
short = {71: "approver named", 74: "request v0", 76: "'outside scope'", 80: "four rules", 82: "register r1", 132: "r2: router",
         138: "r3: fine-tune", 140: "pack v1", 141: "metric check fails", 144: "pack v2", 146: "validator session",
         153: "passed, two conditions"}
role = {141: "blocker", 74: "blocker", 76: "blocker", 153: "approval"}
fig, ax = S.figure(height=4.6)
for i, (d, s) in enumerate(ev):
    r = role.get(d, "evidence")
    ax.plot(d, i, marker="s" if r == "blocker" else "o", color=S.ROLE[r], markersize=8, linestyle="none")
    ax.text(d + 2, i, f"day {d}: {short[d]}", va="center", fontsize=9)
ax.set_yticks([]); ax.invert_yaxis(); ax.set_xlim(65, 200); ax.set_xlabel("engagement day")
ax.spines[["top", "right", "left"]].set_visible(False)
save(fig, 10, data="04-code/ch33/output/review.txt")
