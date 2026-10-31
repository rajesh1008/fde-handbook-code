"""Figure 26.1: from Northlight's 91% to Caldwell's 68%, step by step (Listing 26.1 output)."""
import re
from _common import S, save, text
t = text("vendor_vs_customer")
v = [float(x) for x in re.findall(r"\s([\d.]+)%(?:\s|$)", t)[:4]]
steps = [("Northlight's\ncases and judge", v[0]), ("Anne's\ndocuments", v[1]), ("exact match,\nno judge", v[2]),
         ("Caldwell's\ndefinitions", v[3])]
fig, ax = S.figure(height=3.9)
roles = ["model", "data", "evidence", "blocker"]
prev = None
for i, (lab, val) in enumerate(steps):
    if prev is None:
        ax.bar(i, val, color=S.ROLE["model"], width=0.6)
    else:
        ax.bar(i, prev - val, bottom=val, color=S.ROLE[roles[i]], width=0.6, hatch=S.HATCH[roles[i]],
               edgecolor="white")
        ax.text(i, prev + 1.2, f"{val - prev:+.1f}", ha="center", fontsize=10, color=S.PAL["ink"])
        ax.plot([i - 1 + 0.3, i - 0.3], [prev, prev], color=S.PAL["grey"], lw=0.75)
    prev = val
ax.bar(4, v[3], color=S.ROLE["approval"], width=0.6)
for i, val in ((0, v[0]), (4, v[3])):
    ax.text(i, val + 1.2, f"{val:.1f}%", ha="center", fontsize=11, fontweight="bold", color=S.PAL["ink"])
ax.set_xticks(range(5), [s[0] for s in steps] + ["Caldwell's\nnumber"], fontsize=9)
ax.set_ylim(50, 98); ax.set_ylabel("field accuracy (%)")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 1, data="04-code/ch26/output/vendor_vs_customer.txt")
