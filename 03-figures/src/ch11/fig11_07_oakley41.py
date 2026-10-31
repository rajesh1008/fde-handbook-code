"""Figure 11.7: Sam Oakley's 41 questions by theme: design-changing or evidence only, and answered by day 40."""
from _common import S, save
import oakley41 as O
fig, ax = S.figure(3.9)
for i, (t, n, d, a) in enumerate(O.THEMES):
    ax.barh(i, d, color=S.ROLE["blocker"], edgecolor="white", hatch=S.HATCH["blocker"], height=0.62)
    ax.barh(i, n - d, left=d, color=S.TINT["evidence"], edgecolor=S.ROLE["evidence"], hatch=S.HATCH["evidence"], height=0.62)
    ax.plot([a, a], [i - 0.38, i + 0.38], color=S.PAL["ink"], lw=S.LW["emphasis"])
    ax.text(n + 0.25, i, f"{a} of {n} answered", va="center", fontsize=9.5)
ax.set_yticks(range(len(O.THEMES))); ax.set_yticklabels([t[0] for t in O.THEMES]); ax.invert_yaxis()
ax.set_xlim(0, 14); ax.set_xlabel("questions (black tick: answered by day 40)")
ax.legend(["can change the design", "evidence only"], loc="lower right", fontsize=9.5)
save(fig, 7)
