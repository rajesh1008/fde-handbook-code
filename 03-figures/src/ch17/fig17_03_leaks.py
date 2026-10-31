"""Figure 17.3: results the adjuster may not read, service-account release against rechecked release."""
import re
from _common import S, save, text
t = text("obo_recheck")
unit = int(re.search(r"other unit's claim file: (\d+)", t).group(1))
flag = int(re.search(r"flagged after the 02:00 view was built: (\d+)", t).group(1))
leak_b = int(re.search(r"may not read: (\d+)\n", t.split("Design B")[1]).group(1))
ret = int(re.search(r"results returned (\d+)", t).group(1))
fig, ax = S.figure(height=3.8)
ax.barh([1], [unit], color=S.ROLE["blocker"], edgecolor=S.PAL["ink"], lw=S.LW["data"], hatch="\\\\")
ax.barh([1], [flag], left=[unit], color=S.ROLE["data"], edgecolor=S.PAL["ink"], lw=S.LW["data"], hatch="..")
ax.barh([0], [max(leak_b, 0.001)], color=S.ROLE["approval"], edgecolor=S.PAL["ink"], lw=S.LW["data"])
ax.text(unit / 2, 1.42, f"other unit {unit}", ha="center", fontsize=10)
ax.text(unit + flag / 2, 1.42, f"flagged today {flag}", ha="center", fontsize=10)
ax.text(3, 0, f"{leak_b}", va="center", fontsize=10)
ax.set_yticks([0, 1]); ax.set_yticklabels(["delegation +\nrecheck", "service\naccount"])
ax.set_xlim(0, 125); ax.set_ylim(-0.6, 1.8)
ax.set_xlabel(f"results the adjuster may not read, of {ret:,} returned (600 searches)")
save(fig, 3, data="04-code/ch17/output/obo_recheck.txt")
