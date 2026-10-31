"""Figure 45.5: classify this workflow. The key against two candidates, step by step."""
import sys
from _common import S, save, R, text
sys.path.insert(0, str(R / "04-code/ch45"))
import world as W
from fieldkit.hiring import LEVELS
assert "unsafe 1" in text("whiteboard_c214")
steps = list(W.STEPS)
fig, ax = S.figure(height=4.6)
for i, s in enumerate(steps):
    k = LEVELS.index(W.STEPS[s])
    ax.scatter(k, i, s=260, facecolor="white", edgecolor=S.PAL["ink"], lw=1.5, zorder=2, label="key" if i == 0 else None)
    a = LEVELS.index(W.CLASSIFY["c214"][s]); b = LEVELS.index(W.CLASSIFY["c231"][s])
    ax.scatter(a, i + 0.18, s=60, color=S.ROLE["blocker"], marker="s", zorder=3, label="candidate 214" if i == 0 else None)
    ax.scatter(b, i - 0.18, s=60, color=S.ROLE["approval"], marker="o", zorder=3, label="candidate 231" if i == 0 else None)
    if a > k:
        ax.annotate("", xy=(a - 0.1, i + 0.18), xytext=(k + 0.15, i + 0.18),
                    arrowprops=dict(arrowstyle="-|>", mutation_scale=10, color=S.ROLE["blocker"], lw=S.LW["data"]))
ax.set_yticks(range(len(steps))); ax.set_yticklabels([s.split(" ", 1)[1] for s in steps], fontsize=9.5)
ax.set_xticks(range(len(LEVELS))); ax.set_xticklabels([l.replace(" ", "\n") for l in LEVELS], fontsize=9.5)
ax.invert_yaxis(); ax.set_xlim(-0.5, 4.5); ax.grid(axis="x", color="#DDDDDD", lw=0.5)
ax.legend(fontsize=9, loc="lower left", ncol=3, bbox_to_anchor=(0, -0.32)); ax.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch45/output/whiteboard_c214.txt, whiteboard_c231.txt")
