"""Figure 28.9: red-team escapes by category, suite v2 against v3."""
import re
from _common import S, save, text
t = text("redteam")
blk = {v: t.split(f"\n{v}: ")[1].split("\n\n")[0] for v in ("v2", "v3")}
cats = re.findall(r"^  (.+?)\s+escapes", blk["v2"], re.M)
e = {v: [int(x) for x in re.findall(r"escapes\s+(\d+) / 20", blk[v])] for v in blk}
fig, ax = S.figure(height=4.2)
y = range(len(cats))
ax.barh([i + 0.2 for i in y], e["v2"], height=0.38, color=S.ROLE["blocker"], hatch=S.HATCH["blocker"], edgecolor="white", label="v2 (day 124)")
ax.barh([i - 0.2 for i in y], e["v3"], height=0.38, color=S.ROLE["approval"], edgecolor="white", label="v3 (day 128)")
for i in y:
    ax.text(e["v2"][i] + 0.2, i + 0.2, str(e["v2"][i]), va="center", fontsize=9)
    ax.text(e["v3"][i] + 0.2, i - 0.2, str(e["v3"][i]), va="center", fontsize=9)
ax.set_yticks(list(y), cats, fontsize=9); ax.invert_yaxis()
ax.set_xlabel("attacks that escaped (of 20 per category)"); ax.set_xlim(0, 20)
ax.legend(loc="lower right", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 9, data="04-code/ch28/output/redteam.txt")
