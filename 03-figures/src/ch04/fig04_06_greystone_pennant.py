"""Figure 4.6: Greystone Health and Pennant Logistics at signature, gated score by dimension."""
from _common import S, save, title, DIMS
import matplotlib.pyplot as plt
from checklists import greystone_sales_demo, pennant_sales_demo

vs = [("Greystone Health", greystone_sales_demo().assess(0), "system"),
      ("Pennant Logistics", pennant_sales_demo().assess(0), "data")]
fig, ax = plt.subplots(figsize=(S.WIDTH_IN, 4.2))
w = 0.36
for k, (name, v, role) in enumerate(vs):
    xs = [i + (k - 0.5) * (w + 0.04) for i in range(5)]
    vals = [v.by_dimension[d] for d in DIMS]
    ax.bar(xs, vals, w, color=S.TINT[role], hatch=S.HATCH[role], edgecolor=S.ROLE[role], lw=1.0,
           label=f"{name}: gated {v.gated:.2f}, {len(v.blocking)} blocking")
    for x, val in zip(xs, vals):
        ax.text(x, val + 0.015, f"{val:.2f}", ha="center", fontsize=9)
ax.set_xticks(range(5), ["capability", "workflow", "controls", "ownership", "reconstruct-\nability"], fontsize=9)
ax.set_ylim(0, 0.8); ax.set_ylabel("gated score by dimension")
ax.legend(frameon=False, fontsize=9, loc="upper left")
title(ax, "Same checklist, different failure")
save(fig, 6, data="04-code/ch04/checklists.greystone_sales_demo() and pennant_sales_demo()")
