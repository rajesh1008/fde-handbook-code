"""Figure 32.11: 22 threats by component and category; the agent category is the column STRIDE lacks."""
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from _common import S, save, world
from fieldkit.security import CATEGORIES
tm = world.THREATS
comps = list(dict.fromkeys(t.component for t in tm.threats)); g = tm.grid()
M = np.array([[g[(c, k)] for k in CATEGORIES] for c in comps])
cm = LinearSegmentedColormap.from_list("ev", ["#FFFFFF", S.TINT["evidence"], S.ROLE["evidence"]])
fig, ax = S.figure(height=4.8)
ax.imshow(M, cmap=cm, vmin=0, vmax=3, aspect="auto")
short = ["spoof", "tamper", "repud.", "disclose", "DoS", "privilege", "agent"]
for i in range(len(comps)):
    for j in range(len(CATEGORIES)):
        if M[i, j]:
            ax.text(j, i, str(M[i, j]), ha="center", va="center", fontsize=10, color=S.PAL["ink"], bbox=dict(fc="white", ec="none", pad=1))
ax.add_patch(__import__("matplotlib.patches", fromlist=["R"]).Rectangle((5.5, -0.5), 1, len(comps), fill=False, ec=S.ROLE["blocker"], lw=S.LW["emphasis"]))
ax.set_xticks(range(len(short))); ax.set_xticklabels(short, rotation=30, ha="right"); ax.set_yticks(range(len(comps))); ax.set_yticklabels(comps)
for s in ax.spines.values(): s.set_visible(False)
save(fig, 11, data="04-code/ch32/output/threat_model.txt; world.py THREATS")
