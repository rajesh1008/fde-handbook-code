"""Figure 43.6: margin on Caldwell's 12-hour retainer in the month of a model upgrade, by rollover rule.
Data: retainer.txt, tryit_b.txt."""
import re
from _common import S, save, text
t = text("tryit_b")
vals = [(m.group(1).strip(), float(m.group(2))) for m in re.finditer(r"^(.*?)\s+month 4 .*margin (-?[\d.]+)%", t, re.M)]
fig, ax = S.figure(height=3.8)
cols = [S.ROLE["blocker"], S.ROLE["cost"], S.ROLE["approval"]]
ax.bar(range(len(vals)), [v for _, v in vals], 0.55, color=cols, hatch="--")
for i, (_, v) in enumerate(vals):
    ax.text(i, v + (2 if v >= 0 else -6), f"{v:.1f}%", ha="center", fontsize=10)
ax.axhline(40, color=S.ROLE["blocker"], lw=S.LW["control"], ls=":"); ax.text(2.35, 41.5, "floor", fontsize=9)
ax.axhline(0, color=S.PAL["ink"], lw=S.LW["data"])
ax.set_xticks(range(len(vals))); ax.set_xticklabels(["unlimited", "capped 12 h", "none"])
ax.set_xlabel("rollover of unused hours"); ax.set_ylabel("margin in month 4, %"); ax.set_ylim(-20, 80)
save(fig, 6, data="04-code/ch43/output/tryit_b.txt")
