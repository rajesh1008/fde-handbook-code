"""Figure 28.4: rules by kind and by how they are enforced."""
import re
from _common import S, save, text
t = text("elicit")
enf = {(k, e): int(n) for k, e, n in re.findall(r"(\w+)/([\w-]+) (\d+)", re.search(r"by enforcement:\s+(.*)", t).group(1))}
kinds = ["input", "output", "action", "budget"]
det = [enf.get((k, "deterministic"), 0) for k in kinds]; mod = [enf.get((k, "model-assisted"), 0) for k in kinds]
fig, ax = S.figure(height=3.9)
ax.bar(kinds, det, color=S.ROLE["system"], hatch=S.HATCH["system"], edgecolor="white", label="deterministic check")
ax.bar(kinds, mod, bottom=det, color=S.ROLE["model"], edgecolor="white", label="model-assisted check")
for i, (a, b) in enumerate(zip(det, mod)):
    ax.text(i, a + b + 0.5, f"{a + b}", ha="center", fontsize=10, color=S.PAL["ink"])
ax.set_ylabel("rules"); ax.set_ylim(0, max(a + b for a, b in zip(det, mod)) + 4)
ax.legend(loc="upper right", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 4, data="04-code/ch28/output/elicit.txt")
