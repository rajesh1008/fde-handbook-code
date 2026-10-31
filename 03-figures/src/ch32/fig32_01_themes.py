"""Figure 32.1: what Greystone's 41 questions ask, by theme, and how many can change the design."""
import re
from _common import S, save, text, hbar
rows = re.findall(r"^([a-z ]+?)\s{2,}(\d+)\s+(\d+)\s{2}", text("triage"), re.M)
fig, ax = S.figure(height=4.2)
hbar(ax, [r[0] for r in rows], [[int(r[1]) for r in rows], [int(r[2]) for r in rows]],
     ["asked", "can change the design"], ["evidence", "blocker"], "questions")
ax.legend(loc="lower right", fontsize=9)
save(fig, 1, data="04-code/ch32/output/triage.txt")
