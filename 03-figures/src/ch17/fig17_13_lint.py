"""Figure 17.12: findings in the three-questions document, day 57 against day 63, by question."""
import re
from _common import S, save, text
t = text("env_doc")
v1 = t.split("v2, day 63")[0]
qs = ["where", "identity", "logs"]
c1 = [len(re.findall(rf"^  {q} / ", v1, re.M)) for q in qs]
c2 = [len(re.findall(rf"^  {q} / ", t.split("v2, day 63")[1].split("v2 as signed")[0], re.M)) for q in qs]
fig, ax = S.figure(height=3.8)
x = range(3)
ax.bar([i - 0.2 for i in x], c1, width=0.38, color=S.ROLE["blocker"], edgecolor=S.PAL["ink"], lw=S.LW["data"], hatch="\\\\", label=f"day 57 ({sum(c1)})")
ax.bar([i + 0.2 for i in x], [max(v, 0.04) for v in c2], width=0.38, color=S.ROLE["approval"], edgecolor=S.PAL["ink"], lw=S.LW["data"], label=f"day 63 ({sum(c2)})")
for i, v in enumerate(c1): ax.text(i - 0.2, v + 0.12, str(v), ha="center", fontsize=10)
for i, v in enumerate(c2): ax.text(i + 0.2, v + 0.12, str(v), ha="center", fontsize=10)
ax.set_xticks(list(x)); ax.set_xticklabels(["where does it run?", "whose identity?", "who sees the logs?"])
ax.set_ylabel("lint findings"); ax.set_ylim(0, max(c1) + 1.5); ax.legend(loc="upper right")
save(fig, 13, data="04-code/ch17/output/env_doc.txt")
