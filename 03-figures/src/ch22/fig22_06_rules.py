"""Figure 22.6: exceptions by reconciliation rule, and what the R3 tolerance trades."""
import re
from _common import S, save, text
rr = re.findall(r"(R\d) (\d+) \(", text("routing"))
tc = re.findall(r"R3 ([\d.]+)%\s+matched\s+[\d.]+%\s+person\s+\d+\s+exceptions\s+\d+ \(false\s+(\d+)\)\s+wrong (\d+)", text("tryit_c"))
fig, (a, b) = S.figure(height=4.2, ncols=2)
a.bar([r[0] for r in rr], [int(r[1]) for r in rr], color=S.ROLE["evidence"], edgecolor=S.PAL["ink"], lw=S.LW["data"])
for r in rr:
    a.text(r[0], int(r[1]) + 1.5, r[1], ha="center", fontsize=9, color=S.PAL["ink"])
a.set_ylabel("exceptions in the week"); a.set_ylim(0, 80)
x = [float(t[0]) for t in tc]
b.plot(x, [int(t[1]) for t in tc], marker="o", color=S.ROLE["data"], lw=S.LW["control"], label="false exceptions")
b.plot(x, [int(t[2]) for t in tc], marker="s", color=S.ROLE["blocker"], lw=S.LW["control"], label="silently wrong")
b.set_yscale("symlog", linthresh=10); b.set_xlabel("R3 tolerance (% of contract)"); b.set_ylabel("documents")
b.axvline(0.5, color=S.PAL["slate"], lw=S.LW["data"], ls="--")
b.legend(loc="upper right", fontsize=9)
save(fig, 6, data="04-code/ch22/output/routing.txt and tryit_c.txt")
