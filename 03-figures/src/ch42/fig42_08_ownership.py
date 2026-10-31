"""Figure 42.8: the ownership map on day 14 and day 90 (ownership.py)."""
from _common import S, save, blank
import sys; sys.path.insert(0, str(__import__("_common").R / "04-code/ch42"))
from ownership import at_go_live, timeline
m14 = at_go_live(); m14.leave("Jenna Ruiz")
m90, _ = timeline()
short = {"own-exec": "executive", "own-gold-set": "gold set", "own-operations": "operations", "own-model-risk": "model risk",
         "own-override": "override", "on-call primary": "on-call", "runbook executed": "runbook",
         "drift monitor read": "drift monitor", "change board": "change board", "provider account": "provider account"}
def role(m, h):
    if h.holder == "Northlight": return "blocker"
    if h.item in m.orphans(): return "cost"
    return "approval" if h.deputy else "data"
fig, ax = S.figure(height=5.6); blank(ax, (0, 10), (0, 11.4))
ax.text(1.2, 10.8, "day 14", fontsize=10, weight="bold"); ax.text(6.2, 10.8, "day 90", fontsize=10, weight="bold")
for col, m in ((0.2, m14), (5.2, m90)):
    for i, h in enumerate(m.holdings.values()):
        S.box(ax, col, 9.6 - i * 1.05, 4.4, 0.85, short[h.item], role=role(m, h), fs=9.5)
save(fig, 8, kind="diagram", data="04-code/ch42/ownership.py at_go_live, timeline; output/ownership.txt")
