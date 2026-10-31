"""Figure 43.7: what each lint flags in the managed-service runbooks, v0 and v1. Data: exitcheck_v0.txt, exitcheck_v1.txt."""
import re
from _common import S, save, text
vals = {}
for v in ("v0", "v1"):
    t = text(f"exitcheck_{v}")
    vals[v] = (int(re.search(r"RB5 \(step names the vendor\): (\d+)", t).group(1)),
               int(re.search(r"exit lint \(step touches an asset Pennant does not own\): (\d+)", t).group(1)))
fig, ax = S.figure(height=3.8)
x = [0, 1]
ax.bar([i - 0.18 for i in x], [vals[v][0] for v in ("v0", "v1")], 0.36, color=S.ROLE["evidence"], hatch="xx", label="names the vendor")
ax.bar([i + 0.18 for i in x], [vals[v][1] for v in ("v0", "v1")], 0.36, color=S.ROLE["blocker"], hatch="\\\\", label="vendor-owned asset")
for i, v in enumerate(("v0", "v1")):
    for off, n in ((-0.18, vals[v][0]), (0.18, vals[v][1])):
        ax.text(i + off, n + 0.3, str(n), ha="center", fontsize=10)
ax.set_xticks(x); ax.set_xticklabels(["runbooks v0", "runbooks v1"]); ax.set_ylabel("steps flagged of 16"); ax.set_ylim(0, 17)
ax.legend(fontsize=9, loc="upper right")
save(fig, 7, data="04-code/ch43/output/exitcheck_v0.txt, exitcheck_v1.txt")
