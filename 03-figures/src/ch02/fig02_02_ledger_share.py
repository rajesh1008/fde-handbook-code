"""Figure 2.2: where the hours went against where the deal sheet assumed they would go."""
from _common import S, save, title, FIGSIZE
import matplotlib.pyplot as plt
from hours_ledger import totals, BUCKETS
from contracts import DEAL_SHEET

t = totals(); tot = sum(t.values())
p = DEAL_SHEET["caldwell"]
sheet = dict(discovery=p.discovery_h, access=p.access_h, model=p.model_h, integration=p.integration_h,
             gates=p.gates_h, handover=p.handover_h, blocked=0)
st = sum(sheet.values())
fig, ax = plt.subplots(figsize=FIGSIZE)
ys = range(len(BUCKETS))[::-1]
for y, b in zip(ys, BUCKETS):
    ax.barh(y + 0.18, sheet[b] / st * 100, height=0.34, color=S.ROLE["evidence"], hatch=S.HATCH["evidence"],
            edgecolor="white", label="deal sheet" if b == "discovery" else None)
    ax.barh(y - 0.18, t[b] / tot * 100, height=0.34, color=S.ROLE["cost"], hatch=S.HATCH["cost"],
            edgecolor="white", label="ledger, days 1 to 47" if b == "discovery" else None)
    ax.text(t[b] / tot * 100 + 1, y - 0.18, f"{t[b]/tot:.0%}", va="center", fontsize=9)
    ax.text(sheet[b] / st * 100 + 1, y + 0.18, f"{sheet[b]/st:.0%}", va="center", fontsize=9, color=S.PAL["slate"])
ax.set_yticks(list(ys)); ax.set_yticklabels(BUCKETS)
ax.set_xlabel("share of FDE hours, %"); ax.set_xlim(0, 66)
ax.legend(frameon=False, loc="lower right", fontsize=9)
title(ax, "Model work was 56% of the plan and 23% of the hours")
save(fig, 2)
