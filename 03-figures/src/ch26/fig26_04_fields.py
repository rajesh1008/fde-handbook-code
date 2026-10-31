"""Figure 26.4: Northlight's judge against Anne's adjusters, field by field (same 300 documents)."""
import re
from _common import S, save, text
t = text("vendor_vs_customer")
rows = re.findall(r"^\s+(\w+)\s+judge\s+([\d.]+)%\s+adjusters\s+([\d.]+)%", t, re.M)
rows = sorted(rows, key=lambda r: float(r[1]) - float(r[2]))
fig, ax = S.figure(height=4.6)
for i, (f, j, a) in enumerate(rows):
    j, a = float(j), float(a)
    ax.plot([a, j], [i, i], color=S.PAL["light"], lw=4, zorder=1)
    ax.scatter([j], [i], color=S.ROLE["model"], s=55, zorder=2, label="Northlight's judge" if i == 0 else None)
    ax.scatter([a], [i], color=S.ROLE["blocker"], marker="D", s=50, zorder=2,
               label="Anne's adjusters" if i == 0 else None)
ax.set_yticks(range(len(rows)), [r[0] for r in rows], fontsize=9, family="monospace")
ax.set_xlim(40, 100); ax.set_xlabel("field scored correct (%)")
ax.legend(loc="lower left", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 4, data="04-code/ch26/output/vendor_vs_customer.txt")
