"""Figure 34.10: Caldwell year-one margin (forecast) from the day-136 base through each v3 commitment, and v5."""
import re
from _common import S, save, text
t = text("margin")
base = float(re.search(r"base, day 136 +([\d.-]+)%", t).group(1))
steps = re.findall(r"^  (CA-\d\d\.\d) .+? +(-?[\d.]+)%   -\$([\d,]+)$", t, re.M)
v5 = float(re.search(r"v5 as signed \(day 149\) +([\d.-]+)%", t).group(1))
fig, ax = S.figure(height=4.9)
prev = base
ax.bar(0, base, color=S.ROLE["system"], hatch=S.HATCH["system"], edgecolor="white", width=0.7)
for i, (cid, after, _) in enumerate(steps, 1):
    after = float(after)
    ax.bar(i, after - prev, bottom=prev, color=S.ROLE["blocker"], hatch=S.HATCH["blocker"], edgecolor="white", width=0.7)
    prev = after
ax.bar(len(steps) + 1, v5, color=S.ROLE["approval"], edgecolor="white", width=0.7)
ax.text(len(steps), prev - 6, f"{prev:.1f}%", ha="center", fontsize=9.5)
ax.text(len(steps) + 1, v5 + 2, f"{v5:.1f}%", ha="center", fontsize=9.5)
ax.text(0, base + 2, f"{base:.1f}%", ha="center", fontsize=9.5)
ax.axhline(40, color=S.PAL["ink"], lw=0.75, ls="--"); ax.text(len(steps) + 1.4, 41, "floor 40%", ha="right", fontsize=9)
ax.axhline(0, color=S.PAL["ink"], lw=0.75)
ax.set_xticks(range(len(steps) + 2), ["day 136"] + [c[:5] for c, _, _ in steps] + ["v5"], rotation=60, fontsize=9)
ax.set_ylabel("year-one gross margin, forecast (%)"); ax.set_ylim(-15, 65)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 10, data="04-code/ch34/output/margin.txt")
