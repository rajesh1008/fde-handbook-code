"""Figure 25.9: what the shadow week looks like as one overwritten record and as three joined records."""
import re
from _common import S, save, text
t = text("three_records")
n = int(re.search(r"three records: (\d+)", t).group(1))
acc, ed, rej = map(int, re.search(r"accepted (\d+)\s+edited (\d+)\s+rejected (\d+)", t).groups())
diff = int(re.search(r"final record differs: (\d+)", t).group(1))
miss, slip = map(int, re.search(r"missed (\d+), production keyer slip (\d+)", t).groups())
fig, ax = S.figure(height=3.7)
ax.barh(1, n, color=S.PAL["grey"], height=0.5)
ax.text(n / 2, 1, f"agrees with final: {n:,} of {n:,}", ha="center", va="center", fontsize=10, color=S.PAL["ink"], weight="bold")
segs = [(acc - diff, "accepted, same", S.ROLE["approval"]), (miss, "", S.ROLE["blocker"]), (slip, "", S.ROLE["data"]),
        (ed, "edited", S.ROLE["evidence"]), (rej, "", S.ROLE["cost"])]
left = 0
for w, lab, c in segs:
    ax.barh(0, w, left=left, color=c, height=0.5)
    left += w
ax.text((acc - diff) / 2, 0, f"accepted, same as final: {acc - diff}", ha="center", va="center", fontsize=10, weight="bold",
        color=S.PAL["ink"])
ax.annotate(f"accepted but final differs {diff}:\n{miss} agent errors missed, {slip} keyer slips", xy=(acc - diff + 15, -0.25),
            xytext=(330, -0.95), fontsize=10, color=S.PAL["ink"], arrowprops=dict(arrowstyle="-", color=S.PAL["ink"], lw=0.75))
ax.text(acc + ed / 2, 0.36, f"edited {ed}", ha="center", fontsize=10, color=S.PAL["ink"])
ax.text(n - rej / 2, -0.42, f"rejected {rej}", ha="center", fontsize=10, color=S.PAL["ink"])
ax.set_yticks([1, 0], ["one record,\noverwritten", "three records,\njoined"]); ax.set_ylim(-1.3, 1.5)
ax.set_xlabel(f"proposals, shadow week (of {n:,})"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 9, data="04-code/ch25/output/three_records.txt")
