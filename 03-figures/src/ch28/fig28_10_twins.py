"""Figure 28.10: benign twins refused or routed: a keyword guard against the rule suite."""
import re
from _common import S, save, text
t = text("redteam")
kw = int(re.search(r"keyword guard \+ v2: escapes \d+ of \d+; benign twins refused or routed (\d+)", t).group(1))
v3 = int(re.search(r"\nv3: escapes \d+ of \d+; benign twins refused or routed (\d+)", t).group(1))
kesc = int(re.search(r"keyword guard \+ v2: escapes (\d+)", t).group(1)); v3esc = int(re.search(r"\nv3: escapes (\d+)", t).group(1))
fig, ax = S.figure(height=3.9)
labs = ["keyword guard", "rule suite v3"]
ax.bar([0, 1], [kw, v3], color=[S.ROLE["blocker"], S.ROLE["approval"]], hatch=[S.HATCH["blocker"], ""], edgecolor="white", width=0.55)
for i, (v, e) in enumerate([(kw, kesc), (v3, v3esc)]):
    ax.text(i, v + 1.2, f"{v} of 60 refused\n{e} of 140 attacks escaped", ha="center", fontsize=9)
ax.set_xticks([0, 1], labs); ax.set_ylabel("benign twins refused or routed"); ax.set_ylim(0, 72)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 10, data="04-code/ch28/output/redteam.txt")
