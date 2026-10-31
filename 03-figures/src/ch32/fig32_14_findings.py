"""Figure 32.14: the 12 findings by severity and kind."""
from collections import Counter
from _common import S, save, world
fs = world.findings(); c = Counter((f.severity, f.kind) for f in fs); ks = ["high", "medium", "low"]
fig, ax = S.figure(height=3.8)
e = [c[(k, "evidence")] for k in ks]; d = [c[(k, "design")] for k in ks]
ax.bar(ks, e, color=S.TINT["evidence"], edgecolor=S.ROLE["evidence"], hatch=S.HATCH["evidence"], label="evidence finding")
ax.bar(ks, d, bottom=e, color=S.TINT["blocker"], edgecolor=S.ROLE["blocker"], hatch=S.HATCH["blocker"], label="design finding")
for i in range(3):
    ax.text(i, e[i] + d[i] + 0.15, f"{e[i] + d[i]}", ha="center", fontsize=10)
ax.set_ylabel("findings"); ax.set_ylim(0, 8); ax.legend(fontsize=9, loc="upper left"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 14, data="04-code/ch32/output/review.txt")
