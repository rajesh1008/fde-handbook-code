"""Figure 28.12: cumulative model cost of the lookup loop, without and with budgets."""
import re
from _common import S, save, text
t = text("loop")
cum = [float(x) for x in re.search(r"cumulative cost by call, without budgets: (.*)", t).group(1).split()]
g = re.findall(r"cost line: (\d+) tool calls, [\d,]+ tokens, \$([\d.]+)", t)
gc, gcost = int(g[1][0]), float(g[1][1])
fig, ax = S.figure(height=4.0)
ax.plot(range(1, len(cum) + 1), cum, color=S.ROLE["blocker"], lw=2, label="no budgets: cap at 50, no handoff")
ax.plot(range(1, gc + 1), cum[:gc], color=S.ROLE["approval"], lw=3, label=f"breaker opens at call {gc}: coordinator")
ax.axhline(0.40, color=S.ROLE["cost"], ls="--", lw=1); ax.text(2, 0.47, "B-05 cost budget $0.40", fontsize=9, color=S.ROLE["cost"])
ax.scatter([gc], [gcost], color=S.ROLE["approval"], zorder=3)
ax.set_xlabel("lookup calls"); ax.set_ylabel("cumulative model cost ($)")
ax.legend(loc="upper left", fontsize=9, bbox_to_anchor=(0, 0.92)); ax.spines[["top", "right"]].set_visible(False)
save(fig, 12, data="04-code/ch28/output/loop.txt")
