"""Figure 20.8: field flips between extract-2026-04 and extract-2026-01 on 200 synthetic EU-lane documents."""
import re
from _common import S, save, text
rows = re.findall(r"^  (\w+)\s+lost\s+(\d+)\s+gained\s+(\d+)", text("region_drift"), re.M)
fig, ax = S.figure(height=4.0)
names = [r[0] for r in rows]; lost = [-int(r[1]) for r in rows]; gained = [int(r[2]) for r in rows]
y = range(len(rows))
ax.barh(y, lost, color=S.ROLE["blocker"], edgecolor=S.PAL["ink"], lw=S.LW["data"], label="lost on 2026-01")
ax.barh(y, gained, color=S.ROLE["approval"], edgecolor=S.PAL["ink"], lw=S.LW["data"], label="gained on 2026-01")
ax.axvline(0, color=S.PAL["ink"], lw=S.LW["control"])
ax.set_yticks(list(y)); ax.set_yticklabels(names); ax.invert_yaxis()
ax.set_xlabel("fields changed (left: lost, right: gained)"); ax.set_xlim(-14, 6)
ax.legend(loc="lower left", fontsize=9)
save(fig, 8, data="04-code/ch20/output/region_drift.txt")
