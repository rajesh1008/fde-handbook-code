"""Figure 24.10: distribution of whole-turn latency over 500 turns, three fan-out designs, 4 s budget (fanout.txt)."""
import re
from _common import S, save, text
t = text("fanout")
cdf = {k: [float(x) for x in v.split()] for k, v in re.findall(r"^cdf (\w+): (.+)$", t, re.M)}
ps = list(range(0, 101, 5))
fig, ax = S.figure(height=4.2)
sty = {"sequential": (S.ROLE["blocker"], "-"), "parallel": (S.PAL["slate"], "--"), "timeout": (S.PAL["teal"], "-")}
lab = {"sequential": "sequential", "parallel": "parallel", "timeout": "parallel + 2.5 s timeout"}
for k, xs in cdf.items():
    c, ls = sty[k]
    ax.plot([x / 1000 for x in xs], ps, color=c, ls=ls, lw=S.LW["control"])
    ax.text(xs[17] / 1000 + 0.12, 85 - (8 if k == "timeout" else 0), lab[k], fontsize=10, color=S.PAL["ink"])
ax.axvline(4.0, color=S.PAL["ink"], lw=0.75); ax.axhline(95, color=S.PAL["grey"], lw=0.75, ls=":")
ax.text(4.05, 3, "4 s budget", fontsize=10)
ax.set_xlim(1.5, 10); ax.set_ylim(0, 101); ax.set_xlabel("seconds per turn"); ax.set_ylabel("percent of 500 turns at or below")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 10, data="04-code/ch24/output/fanout.txt")
