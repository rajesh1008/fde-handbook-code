"""Figure 24.12: results the adjuster may not read, by how identity crosses the boundary (identity.txt)."""
import re
from _common import S, save, text
t = text("identity")
refused = int(re.search(r"(\d+)/600 turns refused", t).group(1))
svc = int(re.search(r"nl-brain-svc: (\d+) of", t).group(1))
kinds = dict((k, int(v)) for v, k in [(m[1], m[0]) for m in re.findall(r"(legal hold|siu) (\d+)", t)])
obo = int(re.search(r"recheck:\s+(\d+) results", t).group(1))
fig, ax = S.figure(height=4.0)
ax.bar(0, 0, color=S.PAL["grey"]); ax.text(0, 3, f"0 results:\n{refused}/600 turns\nrefused", ha="center", fontsize=10)
ax.bar(1, kinds["siu"], color=S.TINT["blocker"], edgecolor=S.ROLE["blocker"]); ax.bar(1, kinds["legal hold"], bottom=kinds["siu"], color=S.PAL["plum"])
ax.text(1, kinds["siu"] / 2, f"SIU {kinds['siu']}", ha="center", va="center", fontsize=10, color=S.PAL["ink"],
        bbox=dict(boxstyle="square,pad=0.1", fc=S.TINT["blocker"], ec="none"))
ax.text(1, kinds["siu"] + kinds["legal hold"] / 2, f"legal hold {kinds['legal hold']}", ha="center", va="center", fontsize=10, color="white",
        bbox=dict(boxstyle="square,pad=0.1", fc=S.PAL["plum"], ec="none"))
ax.text(1, svc + 2, f"{svc} of 3,000", ha="center", fontsize=10, weight="bold")
ax.bar(2, obo, color=S.ROLE["approval"]); ax.text(2, 3, f"{obo} of 3,000", ha="center", fontsize=10, weight="bold")
ax.set_xticks([0, 1, 2], ["suite token\nforwarded", "service role", "on behalf of\n+ recheck"])
ax.set_ylim(0, 100); ax.set_ylabel("results shown the adjuster may not read")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 12, data="04-code/ch24/output/identity.txt")
