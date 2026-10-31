"""Figure 36.3: suite v2 (day 126) outcomes by the channel the attack entered through."""
from _common import S, save, text
from collections import defaultdict
c = defaultdict(lambda: defaultdict(int))
for l in text("campaign-v2").splitlines():
    if l.startswith("RT-"):
        ch, oc = l[7:22].strip(), l[34:42].strip()
        c[ch][oc] += 1
chans = ["free text", "scanned letter", "fax cover", "attachment", "metadata"]
assert sum(c[ch]["reached"] for ch in chans) == 14
fig, ax = S.figure(height=4.0)
roles = [("reached", "blocker"), ("blocked", "approval"), ("refused", "model"), ("ignored", "evidence")]
left = [0] * len(chans)
y = list(range(len(chans)))[::-1]
for oc, r in roles:
    vals = [c[ch][oc] for ch in chans]
    ax.barh(y, vals, 0.6, left=left, color=S.ROLE[r], label=oc, edgecolor="white")
    left = [a + b for a, b in zip(left, vals)]
ax.set_yticks(y); ax.set_yticklabels(chans)
ax.set_xlabel("attacks (20 in all)"); ax.set_xlim(0, 7)
ax.legend(fontsize=9.5, loc="lower right", ncol=2); ax.spines[["top", "right"]].set_visible(False)
save(fig, 3, data="04-code/ch36/output/campaign-v2.txt")
