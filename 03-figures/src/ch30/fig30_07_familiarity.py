"""Figure 30.7: familiarity of documents to the training vocabulary, with the 0.95 hold line (Listing 30.4)."""
from _common import S, save, js
import numpy as np
d = js("familiarity"); g = d["groups"]; th = d["threshold"]
fig, ax = S.figure(height=3.9)
rng = np.random.default_rng(9)
cols = ["approval", "evidence", "blocker"]
for i, (name, vals) in enumerate(g.items()):
    v = np.array(vals); y = i + rng.uniform(-0.25, 0.25, len(v))
    ax.scatter(v, y, s=14, color=S.ROLE[cols[i]], linewidths=0)
    S.label(ax, 0.858, i + 0.33, f"{len(v)} documents, {int((v < th).sum())} below line", fs=9)
ax.axvline(th, color=S.PAL["ink"], lw=S.LW["control"], ls="--")
ax.set_yticks(range(len(g)), list(g), fontsize=9); ax.invert_yaxis()
ax.set_xlim(0.855, 1.012); ax.set_xlabel("share of words seen in training")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 7, data="04-code/ch30/output/familiarity.json")
