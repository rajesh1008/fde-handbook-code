"""Figure 4.4: naive and gated readiness for four checklists (the lab's run_readiness and failure injection)."""
from _common import S, save, title
import matplotlib.pyplot as plt
from checklists import demo_as_sold, caldwell, caldwell_projected

cases = [("demo as sold", demo_as_sold().assess(2)), ("Caldwell\nday 10", caldwell(day=10).assess(10)),
         ("projected,\nshadow exit", caldwell_projected().assess(140)),
         ("projected,\nowners removed", caldwell_projected(no_owner=True).assess(140))]
fig, ax = plt.subplots(figsize=(S.WIDTH_IN, 4.2))
w = 0.36
for i, (_, v) in enumerate(cases):
    ax.bar(i - w / 2 - 0.02, v.naive, w, color=S.TINT["evidence"], hatch=S.HATCH["evidence"],
           edgecolor=S.ROLE["evidence"], lw=0.75, label="naive score" if i == 0 else None)
    ax.bar(i + w / 2 + 0.02, v.gated, w, color=S.ROLE["approval"], edgecolor="white",
           label="gated score" if i == 0 else None)
    ax.text(i - w / 2 - 0.02, v.naive + 0.02, f"{v.naive:.2f}", ha="center", fontsize=9)
    ax.text(i + w / 2 + 0.02, v.gated + 0.02, f"{v.gated:.2f}", ha="center", fontsize=9)
    ax.text(i, 1.08, v.label, ha="center", fontsize=9, weight="bold")
ax.axhline(0.8, color=S.PAL["ink"], lw=1.0, ls="--")
ax.text(-0.62, 0.82, "gate line 0.8", fontsize=9, ha="left")
ax.set_xticks(range(4), [c[0] for c in cases], fontsize=9)
ax.set_ylim(0, 1.16); ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]); ax.set_ylabel("readiness score")
ax.legend(frameon=False, fontsize=9, loc="upper left", bbox_to_anchor=(0.0, 0.70))
title(ax, "The naive score cannot see a missing owner; the gated verdict can")
save(fig, 4, data="04-code/ch04/run_readiness.py and failure_no_owner.py via checklists.py")
