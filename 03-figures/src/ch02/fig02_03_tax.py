"""Figure 2.3: Pennant's year-one margin as the integration tax rises."""
from _common import S, save, title, FIGSIZE
import matplotlib.pyplot as plt
from contracts import CONTRACTS, FIELD_ESTIMATE
from margin import year_one, with_

c, base = CONTRACTS["pennant"], FIELD_ESTIMATE["pennant"]
xs = [x / 10 for x in range(0, 41)]
ms = [year_one(c, with_(base, integration_tax=x)).margin * 100 for x in xs]
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.plot(xs, ms, color=S.ROLE["cost"], lw=2.4, label="year-one margin")
for x, lab in [(0.5, "deal sheet 0.5"), (2.0, "field estimate 2.0")]:
    m = year_one(c, with_(base, integration_tax=x)).margin * 100
    ax.plot(x, m, "o", color=S.ROLE["cost"]); ax.annotate(f"{lab}: {m:.0f}%", (x, m), (x + 0.15, m + 3), fontsize=9)
ax.axhline(60, color=S.ROLE["approval"], ls="--", lw=1.3); ax.text(3.95, 61, "target 60%", ha="right", fontsize=9, color=S.PAL["ink"])
ax.axhline(40, color=S.ROLE["blocker"], ls=":", lw=1.3); ax.text(3.95, 41, "floor 40%", ha="right", fontsize=9, color=S.PAL["ink"])
ax.set_xlabel("integration tax: integration hours per model-work hour"); ax.set_ylabel("year-one gross margin, %")
ax.set_ylim(20, 70)
title(ax, "Pennant Logistics: each point of tax costs about six margin points")
save(fig, 3)
