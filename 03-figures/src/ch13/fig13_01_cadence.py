"""Two-week cadence: the events on each of the ten working days."""
from _common import S, save, plt
fig, ax = S.figure(3.9)
rows = [("planning", [1], "approval"), ("daily coordination", list(range(1, 11)), "evidence"),
        ("refinement", [3, 8], "system"), ("architecture and control clinic", [2, 4, 7, 9], "data"),
        ("mid-sprint playback", [6, 7], "model"), ("review and acceptance", [10], "approval"),
        ("retrospective", [10], "evidence")]
for r, (name, days, role) in enumerate(rows):
    y = len(rows) - r
    for d in days:
        ax.add_patch(plt.Rectangle((d - 0.42, y - 0.32), 0.84, 0.64, facecolor=S.ROLE[role],
                                   hatch=S.HATCH[role], edgecolor="white"))
    ax.text(0.3, y, name, ha="right", va="center", fontsize=9)
ax.set_xlim(0.3, 10.6); ax.set_ylim(0.3, len(rows) + 0.7)
ax.set_xticks(range(1, 11)); ax.set_xlabel("sprint working day"); ax.set_yticks([])
for s in ("left", "right", "top"): ax.spines[s].set_visible(False)
save(fig, 1, kind="diagram")
