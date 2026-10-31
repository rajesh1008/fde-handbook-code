"""Figure 41.6: where Caldwell's 14 alert rules land; A-07 is the one routed to a Northlight address."""
from _common import S, save, text
from collections import Counter
rows = [l.split() for l in text("routes_v1").splitlines() if l.startswith("A-")]
dest = Counter(r[-2] for r in rows)
bad = {r[-2] for r in rows if r[-1] == "VENDOR"}
fig, ax = S.figure(height=3.9)
names = sorted(dest, key=lambda d: (d in bad, -dest[d]))
for i, d in enumerate(names):
    r = "blocker" if d in bad else "system"
    ax.barh(i, dest[d], color=S.ROLE[r], hatch=S.HATCH[r], ec="white")
    ax.text(dest[d] + 0.1, i, str(dest[d]) + ("  A-07" if d in bad else ""), va="center", fontsize=9)
ax.set_yticks(range(len(names))); ax.set_yticklabels([d.split("@")[0] + ("@northlight" if d in bad else "") for d in names])
ax.invert_yaxis(); ax.set_xlabel("alert rules"); ax.set_xlim(0, 7.5); ax.spines[["top", "right"]].set_visible(False)
save(fig, 6, data="04-code/ch41/output/routes_v1.txt")
