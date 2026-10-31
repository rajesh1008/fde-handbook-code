"""Figure 21.12: cost of starting lineage on day D, in hours and in outputs that can never be reconstructed."""
import re
from _common import S, save, text
rows = [tuple(map(int, m)) for m in re.findall(r"day\s+(\d+)\s+\|\s+(\d+) \|\s+(\d+) \|\s+(\d+)", text("retrofit"))]
day = [r[0] for r in rows]; hrs = [r[1] for r in rows]; lost = [r[3] for r in rows]
fig, (a, b) = S.figure(height=4.4, nrows=2, sharex=True)
a.plot(day, hrs, marker="o", color=S.ROLE["cost"], lw=S.LW["control"]); a.set_ylabel("hours")
a.text(2, hrs[0] + 14, f"day 0: {hrs[0]} h", fontsize=10, color=S.PAL["ink"])
b.bar(day, lost, width=9, color=S.ROLE["blocker"]); b.set_ylabel("outputs lost")
b.set_xlabel("engagement day lineage starts")
for x in (a, b):
    x.spines[["top", "right"]].set_visible(False)
save(fig, 12, data="04-code/ch21/output/retrofit.txt")
