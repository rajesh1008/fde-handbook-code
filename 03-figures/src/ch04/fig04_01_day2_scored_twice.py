"""Figure 4.1: the day-2 demo scored twice, per field and per intake channel (Chapter 3 lab output)."""
import re
from _common import S, save, title, R
import matplotlib.pyplot as plt

txt = (R / "04-code/ch03/output/day2_demo_score.txt").read_text()
rows = re.findall(r"^(\w+)\s+(\d+)/10\s+(\d+)/10$", txt, re.M)
chan = re.findall(r"^\s+(email|fax|mail)\s+\d+ docs\s+\d+/\d+\s+(\d+)%$", txt, re.M)
assert len(rows) == 10 and len(chan) == 3
fig, (a1, a2) = plt.subplots(1, 2, figsize=(S.WIDTH_IN, 4.6), gridspec_kw=dict(width_ratios=[2.3, 1]))
names = [r[0] for r in rows][::-1]
demo = [int(r[1]) for r in rows][::-1]
cust = [int(r[2]) for r in rows][::-1]
y = range(len(names))
a1.barh(y, demo, color="white", edgecolor=S.PAL["grey"], lw=1.2, height=0.75, label="demo set, self-scored")
a1.barh(y, cust, color=S.ROLE["evidence"], hatch=S.HATCH["evidence"], edgecolor="white", height=0.5,
        label="Caldwell, scored by Anne Kessler")
for i, v in enumerate(cust):
    a1.text(10.3, i, f"{v}", va="center", fontsize=9)
a1.set_yticks(list(y), names, fontsize=9, family="monospace")
a1.set_xlim(0, 11.2); a1.set_xticks([0, 5, 10]); a1.set_xlabel("fields right, of 10 documents")
a1.legend(loc="upper center", bbox_to_anchor=(0.45, -0.16), frameon=False, fontsize=9, ncol=1)
a2.bar(range(3), [int(c[1]) for c in chan], color=S.ROLE["evidence"], hatch=S.HATCH["evidence"],
       edgecolor="white", width=0.6)
for i, c in enumerate(chan):
    a2.text(i, int(c[1]) + 2, f"{c[1]}%", ha="center", fontsize=9)
a2.axhline(98, color=S.PAL["ink"], lw=1.2, ls="--")
a2.text(1, 101, "demo set 98%", ha="center", fontsize=9)
a2.set_xticks(range(3), [c[0] for c in chan]); a2.set_ylim(0, 112); a2.set_yticks([0, 25, 50, 75, 100])
a2.set_ylabel("fields right, %")
title(a1, "The same demo, scored twice")
save(fig, 1, data="04-code/ch03/output/day2_demo_score.txt (Chapter 3 lab; scorer Anne Kessler)")
