"""Figure 21.13: lineage for every output against decisions only: storage per month and audit questions answerable."""
import re
from _common import S, save, text
t = text("granularity")
rows = re.findall(r"^(every output|decisions only)\s+([\d.]+) MB.*?(\d+)/(\d+)", t, re.M)
fig, (a, b) = S.figure(height=3.7, ncols=2)
names = ["every\noutput", "decisions\nonly"]; cols = [S.ROLE["evidence"], S.ROLE["data"]]
a.bar(names, [float(r[1]) for r in rows], color=cols); a.set_ylabel("MB per month")
b.bar(names, [100 * int(r[2]) / int(r[3]) for r in rows], color=cols); b.set_ylabel("questions answerable (%)"); b.set_ylim(0, 110)
for x, r in zip(range(2), rows):
    a.text(x, float(r[1]) + 1, f"{float(r[1]):.0f}", ha="center", fontsize=10, color=S.PAL["ink"])
    b.text(x, 100 * int(r[2]) / int(r[3]) + 2, f"{r[2]}/{r[3]}", ha="center", fontsize=10, color=S.PAL["ink"])
for x in (a, b):
    x.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
save(fig, 13, data="04-code/ch21/output/granularity.txt")
