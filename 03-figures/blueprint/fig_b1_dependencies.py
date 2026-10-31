"""Figure B.1: chapter dependency map (Blueprint). Reads 00-plan/blueprint.json written by make_blueprint.py."""
import json, sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
sys.path.insert(0, "/workspace/books/fde-handbook/05-build/design")
ROOT = "/workspace/books/fde-handbook"
bp = json.load(open(f"{ROOT}/00-plan/blueprint.json"))["chapters"]
PARTS = [(1,5,"I","Role and economics"),(6,14,"II","Discovery and scoping"),(15,22,"III","Data and systems"),(23,31,"IV","Building on site"),
         (32,38,"V","Gates"),(39,43,"VI","Pilot to hand-over"),(44,47,"VII","Practice"),(48,52,"VIII","Four deployments")]
COL = ["#1F3A5F","#0F7C80","#D99A1E","#5A6F9C","#E05A47","#3A8F4B","#7B4B83","#1E2329"]
try:
    import fde_style; fde_style.apply()
except Exception:
    plt.rcParams.update({"font.family": "DejaVu Sans"})
pos = {}
for k,(a,b,r,name) in enumerate(PARTS):
    for j,n in enumerate(range(a,b+1)):
        pos[n] = (k*3.0, -j*1.0)
fig, ax = plt.subplots(figsize=(20, 9), dpi=110)
for n, c in bp.items():
    n = int(n); x1,y1 = pos[n]
    for d in c["deps"]:
        x0,y0 = pos[d]
        same = abs(x0-x1) < .01
        if same:
            ax.annotate("", xy=(x1-1.15,y1), xytext=(x0-1.15,y0), arrowprops=dict(arrowstyle="-|>", color="#9AA5B4", lw=.7, connectionstyle="arc3,rad=0.5", shrinkA=2, shrinkB=2))
        else:
            ax.annotate("", xy=(x1-1.15,y1), xytext=(x0+1.15,y0), arrowprops=dict(arrowstyle="-|>", color="#C9D0D8", lw=.55, alpha=.7, connectionstyle="arc3,rad=0.08", shrinkA=1, shrinkB=1))
for k,(a,b,r,name) in enumerate(PARTS):
    ax.text(k*3.0, 1.15, f"Part {r}", ha="center", fontsize=13, weight="bold", color=COL[k])
    ax.text(k*3.0, .72, name, ha="center", fontsize=10, color="#1E2329")
    for n in range(a,b+1):
        x,y = pos[n]; c = bp[str(n)]
        ax.add_patch(FancyBboxPatch((x-1.15,y-.36), 2.3, .72, boxstyle="round,pad=0.02,rounding_size=0.12", fc=COL[k], ec="white", lw=1))
        t = c["title"]; t = t if len(t) <= 24 else t[:23].rstrip(" ,:")+"…"
        ax.text(x-1.07, y+.08, f"Ch{n}", color="white", fontsize=9, weight="bold", va="center")
        ax.text(x+1.07, y+.08, f"{c['total']/1000:.1f}k", color="white", fontsize=8, va="center", ha="right")
        ax.text(x-1.07, y-.18, t, color="white", fontsize=7, va="center")
ax.set_xlim(-1.4, 7*3.0+1.3); ax.set_ylim(-8.6, 1.5); ax.axis("off")
ax.set_title("Chapter dependencies: arrows run from prerequisite to dependent chapter; box shows planned words", fontsize=12, loc="left", color="#1E2329")
fig.text(.01,.01,"Generated from 00-plan/blueprint.json (Stage 1). Within-Part arrows curve on the left edge; cross-Part arrows run left to right.", fontsize=8, color="#5A6F9C")
out = f"{ROOT}/03-figures/blueprint/fig-b1-dependencies.png"
fig.savefig(out, bbox_inches="tight", facecolor="white"); print(out)
