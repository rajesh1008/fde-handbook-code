"""Figure 4.3: Caldwell's gap register on day 10, claims made against proofs held, by dimension."""
from collections import Counter
from _common import S, save, title, DIMS
import matplotlib.pyplot as plt
from gap_register import DEMO_CLAIMS
from checklists import caldwell

claims = Counter(d for _, _, d, _ in DEMO_CLAIMS)
c = caldwell(day=10)
st = {d: Counter(p.counted(c.customer_people) for p in c.proofs.values() if p.dimension == d) for d in DIMS}
fig, ax = plt.subplots(figsize=(S.WIDTH_IN, 4.2))
x = range(len(DIMS)); w = 0.36
ax.bar([i - w / 2 - 0.02 for i in x], [claims[d] for d in DIMS], w, color=S.ROLE["model"], edgecolor="white",
       label="sales claims made")
bottom = [0] * 5
for key, col, hat, lab in (("held", S.ROLE["approval"], "", "proofs held"),
                           ("partial", S.TINT["data"], "..", "proofs partial"),
                           ("missing", S.TINT["blocker"], "\\\\", "proofs missing")):
    vals = [st[d][key] for d in DIMS]
    ax.bar([i + w / 2 + 0.02 for i in x], vals, w, bottom=bottom, color=col, hatch=hat,
           edgecolor=S.ROLE["blocker"] if key == "missing" else (S.ROLE["data"] if key == "partial" else "white"),
           lw=0.75, label=lab)
    bottom = [b + v for b, v in zip(bottom, vals)]
for i, d in enumerate(DIMS):
    ax.text(i - w / 2 - 0.02, claims[d] + 0.15, str(claims[d]), ha="center", fontsize=9)
ax.set_xticks(list(x), ["capability", "workflow", "controls", "ownership", "reconstruct-\nability"], fontsize=9)
ax.set_ylabel("count"); ax.set_ylim(0, 9)
ax.legend(frameon=False, fontsize=9, loc="upper right")
title(ax, "Claims pile up on capability; proofs are spread across five dimensions")
save(fig, 3, data="04-code/ch04/gap_register.py and checklists.caldwell(day=10)")
