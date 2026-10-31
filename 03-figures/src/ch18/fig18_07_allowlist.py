"""Figure 18.7: denied requests from a new runner address, naive retries against fieldkit's stop."""
import re
from _common import S, save, text
fig, ax = S.figure(height=3.9)
rows = re.findall(r"^(\w+)\s+denied requests\s+(\d+); (.+)$", text("allowlist"), re.M)
names = [r[0] for r in rows]; vals = [int(r[1]) for r in rows]
ax.barh(range(len(vals)), vals, color=[S.ROLE["blocker"], S.ROLE["system"]], edgecolor=S.PAL["ink"], lw=S.LW["data"])
for i, (v, r) in enumerate(zip(vals, rows)):
    ax.text(v + 3, i, f"{v} ({r[2]})", va="center", fontsize=10)
ax.axvline(100, color=S.PAL["ink"], ls="--", lw=S.LW["control"]); ax.text(101, 1.35, "gateway security alert at 100 per hour", fontsize=9)
ax.set_yticks(range(len(vals))); ax.set_yticklabels([f"{n} adapter" for n in names]); ax.set_xlim(0, 230)
ax.set_xlabel("requests denied by the allowlist (40 test calls)"); ax.set_ylim(-0.6, 1.7)
save(fig, 7, data="04-code/ch18/output/allowlist.txt")
