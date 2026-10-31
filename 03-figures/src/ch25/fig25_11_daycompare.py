"""Figure 25.11: the same 231 documents through the first agent loop and through the executor."""
import re
from _common import S, save, text
a, b = text("day109_retry"), text("day109_fixed")
dup = int(re.search(r"duplicates \(policy, loss date, claimant\): (\d+)", a).group(1))
g = int(re.search(r"guessed cause code: (\d+)", a).group(1))
openn = int(re.search(r"open claims (\d+)", a).group(1))
open2 = int(re.search(r"open claims (\d+)", b).group(1)); held = int(re.search(r"'held': (\d+)", b).group(1))
fig, ax = S.figure(height=3.7)
cats = ["duplicate claims", "guessed cause codes", "held for a person"]
v1, v2 = [dup, g, 0], [0, 0, held]
x = range(3)
ax.bar([i - 0.2 for i in x], v1, 0.38, color=S.ROLE["blocker"], hatch="\\\\", edgecolor=S.PAL["ink"], lw=0.5,
       label=f"first loop ({openn} open claims)")
ax.bar([i + 0.2 for i in x], v2, 0.38, color=S.ROLE["approval"], edgecolor=S.PAL["ink"], lw=0.5,
       label=f"executor ({open2} open claims)")
for i in x:
    ax.text(i - 0.2, v1[i] + 0.2, str(v1[i]), ha="center", fontsize=10, color=S.PAL["ink"])
    ax.text(i + 0.2, v2[i] + 0.2, str(v2[i]), ha="center", fontsize=10, color=S.PAL["ink"])
ax.set_xticks(list(x), cats); ax.set_ylabel("claims, day 109 replay"); ax.set_ylim(0, 14)
ax.legend(loc="upper right", fontsize=9.5); ax.spines[["top", "right"]].set_visible(False)
save(fig, 11, data="04-code/ch25/output/day109_retry.txt, day109_fixed.txt")
