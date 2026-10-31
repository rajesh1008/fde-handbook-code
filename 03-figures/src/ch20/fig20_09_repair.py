"""Figure 20.9: findings reported at each repair iteration, partial rescan against full rescan (Greystone)."""
import re
from _common import S, save, text
t = text("iac_check")
blocks = t.split("--- repair loop, ")[1:]
fig, ax = S.figure(height=3.9)
for b, role, mk, lab in zip(blocks, ["blocker", "approval"], ["o", "s"], ["failing rules only", "every rule"]):
    its = [(int(i), int(n)) for i, n in re.findall(r"iteration (\d+): findings (\d+)", b)]
    ax.plot([i for i, _ in its], [n for _, n in its], marker=mk, color=S.ROLE[role], lw=S.LW["control"], label=f"rescan {lab}")
    left = int(re.search(r"full scan of the result: (\d+)", b).group(1))
    if left:
        ax.scatter([its[-1][0]], [left], marker="x", s=60, color=S.PAL["coral"], zorder=5)
        ax.text(its[-1][0] + 0.08, left + 0.3, "still there: diagnostics", fontsize=10)
ax.set_xticks([1, 2, 3]); ax.set_xlabel("repair iteration"); ax.set_ylabel("findings reported"); ax.set_ylim(-0.3, 7)
ax.legend(loc="upper right", fontsize=9)
save(fig, 9, data="04-code/ch20/output/iac_check.txt")
