"""Figure 16.10: the 300-file gold-set plan: population share against drawn share by stratum."""
import re
from _common import S, save, text
fig, ax = S.figure(height=4.2)
rows = [(m.group(1).strip(), int(m.group(2).replace(",", "")), int(m.group(3)), float(m.group(4)))
        for m in re.finditer(r"^\s{2}([a-z ,]+?)\s{2,}([\d,]+)\s+(\d+)\s+(\d\.\d\d)$", text("sample_plan"), re.M)]
P = sum(r[1] for r in rows); N = sum(r[2] for r in rows)
rows = rows[::-1]
for y, (s, p, n, w) in enumerate(rows):
    ax.barh(y + 0.18, p / P * 100, height=0.34, color=S.TINT["evidence"], edgecolor=S.ROLE["evidence"], hatch=S.HATCH["evidence"], lw=S.LW["data"])
    ax.barh(y - 0.18, n / N * 100, height=0.34, color=S.ROLE["data"], edgecolor=S.ROLE["data"])
    ax.text(max(p / P, n / N) * 100 + 0.6, y, f"{n} drawn, weight {w:.2f}", va="center", fontsize=9)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=9.5)
ax.set_xlim(0, 30); ax.set_xlabel("share (%)")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=S.TINT["evidence"], edgecolor=S.ROLE["evidence"], hatch=S.HATCH["evidence"], label=f"quarter's files ({P:,})"),
                   Patch(facecolor=S.ROLE["data"], label=f"gold-set draw ({N})")], loc="lower right", frameon=True,
          edgecolor=S.PAL["light"], fontsize=9)
save(fig, 10, data="04-code/ch16/output/sample_plan.txt")
