"""Figure 25.17: duplicates against the lost-response rate, key per call and key per intent (Try It Yourself a)."""
import re
from _common import S, save, text
rows = [tuple(map(int, m)) for m in re.findall(r"lost 1 in\s+(\d+): duplicates key-per-call\s+(\d+)\s+key-per-intent (\d+)", text("tryit_a"))]
rate = [100 / r[0] for r in rows]
fig, ax = S.figure(height=3.7)
ax.plot(rate, [r[1] for r in rows], color=S.ROLE["blocker"], lw=2.0, marker="o", ms=4)
ax.plot(rate, [r[2] for r in rows], color=S.ROLE["approval"], lw=2.0, marker="s", ms=4, ls="--")
ax.text(rate[-1] - 1, rows[-1][1] - 5, "key per call", fontsize=10, ha="right", color=S.PAL["ink"])
ax.text(rate[-1] - 1, 2.5, "key per intent", fontsize=10, ha="right", color=S.PAL["ink"])
ax.set_xlabel("responses lost (%)"); ax.set_ylabel("duplicate claims"); ax.set_ylim(0, 45)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 17, data="04-code/ch25/output/tryit_a.txt")
