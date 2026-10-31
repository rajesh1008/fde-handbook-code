"""Figure 19.18: Pennant phasing options from the day-24 estimate; phase one is option B."""
from _common import S, save
fig, ax = S.figure(height=3.9)
opts = [("A: all 41 layouts", 1500, "cost"), ("B: top 12, 76% of volume", 886, "approval")]
for i, (t, h, r) in enumerate(opts):
    ax.barh(i, h, color=S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r], lw=S.LW["emphasis"] if i else 0.75)
    ax.text(h + 20, i, f"{h:,} h", va="center", fontsize=10)
ax.set_yticks([0, 1]); ax.set_yticklabels([o[0] for o in opts]); ax.invert_yaxis()
ax.set_xlim(0, 1800); ax.set_xlabel("estimated engineering hours")
save(fig, 18, data="Chapter 10 day-24 estimate (04-code/ch10 output)")
