"""Figure 16.16: left, what the pattern scrub left behind; right, rows suppressed for k = 5 by table grain."""
import re
from _common import S, save, text
t = text("deid_attack")
kinds = [(k.replace("_", " ").replace(" name", ""), int(v)) for k, v in re.findall(r"(\w+) (\d+)", t.split("each kind:")[1].split("\n")[0])]
opts = [(g, f, int(n)) for g, f, n in re.findall(r"^\s{2}(month|quarter|no date)\s+(.+?)\s+suppressed (\d+)", t, re.M)]
fig, (a1, a2) = S.figure(height=4.0, ncols=2)
for y, (k, v) in enumerate(kinds[::-1]):
    a1.barh(y, v, color=S.TINT["cost"], edgecolor=S.ROLE["cost"], hatch=S.HATCH["cost"], lw=S.LW["data"], height=0.6)
    a1.text(v + 2, y, str(v), va="center", fontsize=9)
a1.set_yticks(range(len(kinds))); a1.set_yticklabels([k for k, _ in kinds[::-1]], fontsize=9.5)
a1.set_xlim(0, 100); a1.set_xlabel("documents leaking (of 200)")
labs = ["month\n+ town", "quarter\n+ town", "quarter\nonly", "town\nonly"]
for x, (g, f, n) in enumerate(opts):
    role = "evidence" if x == len(opts) - 1 else "blocker"
    a2.bar(x, n, color=S.TINT[role], edgecolor=S.ROLE[role], hatch=S.HATCH[role], lw=S.LW["data"], width=0.6)
    a2.text(x, n + 2, str(n), ha="center", fontsize=9)
a2.set_xticks(range(len(opts))); a2.set_xticklabels(labs, fontsize=9)
a2.set_ylim(0, 105); a2.set_ylabel("rows suppressed (of 105)")
fig.tight_layout()
save(fig, 16, data="04-code/ch16/output/deid_attack.txt")
