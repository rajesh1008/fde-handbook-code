"""Figure 16.7: population stability index per label-free feature, synthetic v1 and v2 against the real 200."""
from _common import S, save, psi_table
fig, ax = S.figure(height=4.2)
v1, v2 = psi_table()
feats = sorted(v1, key=v1.get)
for y, f in enumerate(feats):
    ax.barh(y + 0.18, v1[f], height=0.34, color=S.TINT["cost"], edgecolor=S.ROLE["cost"], hatch=S.HATCH["cost"], lw=S.LW["data"])
    ax.barh(y - 0.18, max(v2[f], 0.02), height=0.34, color=S.ROLE["evidence"], edgecolor=S.ROLE["evidence"])
    ax.text(v1[f] + 0.05, y + 0.18, f"{v1[f]:.2f}", va="center", fontsize=9)
    ax.text(0.32, y - 0.18, f"{v2[f]:.2f}", va="center", fontsize=9)
ax.axvline(0.25, color=S.PAL["ink"], lw=S.LW["data"], ls="--"); ax.text(0.3, len(feats) - 0.45, "fail above 0.25", fontsize=9)
ax.set_yticks(range(len(feats))); ax.set_yticklabels(feats, fontsize=9.5)
ax.set_xlim(0, 5); ax.set_xlabel("population stability index")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=S.TINT["cost"], edgecolor=S.ROLE["cost"], hatch=S.HATCH["cost"], label="synthetic v1"),
                   Patch(facecolor=S.ROLE["evidence"], label="synthetic v2")], loc="lower right", frameon=True,
          edgecolor=S.PAL["light"], fontsize=9)
save(fig, 7, data="04-code/ch16/output/represent.txt")
