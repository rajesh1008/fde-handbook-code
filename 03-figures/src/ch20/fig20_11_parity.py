"""Figure 20.11: parity checks passed on each estate, by engagement day."""
import re
from _common import S, save, text
t = text("parity")
fig, ax = S.figure(height=3.9)
for blk, role, mk in zip(t.split("--- ")[1:4], ["evidence", "system", "data"], ["D", "o", "s"]):
    name = blk.split(" ---")[0]
    pts = [(int(d), int(n)) for d, n in re.findall(r"day\s+(\d+)\s+(\d+)/14", blk)]
    xs = [p[0] for p in pts] + [122]; ys = [p[1] for p in pts] + [pts[-1][1]]
    ax.step(xs, ys, where="post", color=S.ROLE[role], lw=S.LW["control"], marker=mk, label=name)
ax.axhline(14, color=S.PAL["ink"], lw=S.LW["data"], ls="--")
ax.set_xlabel("engagement day"); ax.set_ylabel("checks passed of 14"); ax.set_ylim(0, 15); ax.set_xlim(99, 122)
ax.legend(loc="lower left", fontsize=9)
save(fig, 11, data="04-code/ch20/output/parity.txt")
