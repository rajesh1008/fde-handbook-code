"""Figure 22.3: what the door did with each channel under pennant-qs-1.0."""
import re
from _common import S, save, text
rows = re.findall(r"^(edi|scan|photo)\s+(\d+)\s+(\d+)\s+(\d+)$", text("breakdown"), re.M)
fig, ax = S.figure(height=4.0)
y = list(range(len(rows)))
left = [0.0] * len(rows)
for j, (name, role) in enumerate([("accepted", "approval"), ("request to sender", "data"), ("rejected, resend", "blocker")]):
    tot = [sum(int(v) for v in r[1:]) for r in rows]
    vals = [100 * int(r[j + 1]) / t for r, t in zip(rows, tot)]
    ax.barh(y, vals, left=left, color=S.ROLE[role], edgecolor=S.PAL["ink"], lw=S.LW["data"], label=name)
    left = [a + b for a, b in zip(left, vals)]
ax.set_yticks(y); ax.set_yticklabels([f"{r[0]} ({sum(int(v) for v in r[1:])})" for r in rows]); ax.invert_yaxis()
ax.set_xlim(0, 100); ax.set_xlabel("share of the channel's documents (%)")
ax.legend(loc="lower left", fontsize=9, ncol=3, bbox_to_anchor=(0, -0.42))
save(fig, 3, data="04-code/ch22/output/breakdown.txt")
