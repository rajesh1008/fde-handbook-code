"""Figure 44.11: peak load before and after the rotation policy, and the effect of overnight rota depth."""
from _common import S, save, text
import re, numpy as np
rep = [l for l in text("rotation").splitlines() if "peak" in l]
ppl = [l.split("peak")[0].strip() for l in rep]
ab = [list(map(float, re.findall(r"peak ([\d.]+) -> ([\d.]+)", l)[0])) for l in rep]
dep = [(int(m.group(1)), float(m.group(2))) for m in re.finditer(r"depth (\d): peak ([\d.]+)", text("tryit_c"))]
fig, (a1, a2) = S.figure(height=3.9, ncols=2)
x = np.arange(len(ppl))
a1.bar(x - 0.2, [v[0] for v in ab], 0.38, color=S.ROLE["blocker"], hatch=S.HATCH["blocker"], ec="white", label="as lived")
a1.bar(x + 0.2, [v[1] for v in ab], 0.38, color=S.ROLE["approval"], ec="white", label="under policy")
a1.set_xticks(x); a1.set_xticklabels([p.replace(" ", "\n") for p in ppl], fontsize=9); a1.set_ylabel("peak load index")
a1.legend(fontsize=9); a1.set_ylim(0, 5.6)
a2.bar([str(d) for d, _v in dep], [v for _d, v in dep], 0.5, color=S.ROLE["system"], hatch=S.HATCH["system"], ec="white")
a2.set_xlabel("people on the overnight rota"); a2.set_ylim(0, 5.6)
for a in (a1, a2):
    a.axhline(3.0, color=S.ROLE["blocker"], lw=0.75, ls=":"); a.spines[["top", "right"]].set_visible(False)
save(fig, 11, data="04-code/ch44/output/rotation.txt, tryit_c.txt")
