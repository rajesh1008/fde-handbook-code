"""Pennant: from a pinned speed item to a returned Architecture Review."""
from _common import S, save, plt
fig, ax = S.figure(3.9)
ev = [(29, "sprint 2 planned:\nP-05 pinned", "cost"), (40, "operations review:\n11 s to 4 s", "approval"),
      (42, "review: 3 items\naccepted", "evidence"), (46, "Architecture Review\nreturned: P-02", "blocker"),
      (60, "re-held after\nsprint 3", "system")]
ax.plot([26, 63], [0, 0], color=S.PAL["ink"], lw=S.LW["control"])
place = [(1, 0.5, "center"), (-1, 0.5, "right"), (1, 1.05, "center"), (-1, 0.5, "left"), (1, 0.5, "center")]
for (d, t, role), (up, hgt, ha) in zip(ev, place):
    ax.plot([d, d], [0, hgt * up], color=S.ROLE[role], lw=S.LW["control"])
    ax.plot(d, 0, marker="s", color=S.ROLE[role], ms=8)
    ax.text(d, (hgt + 0.07) * up, f"day {d}: " + t, ha=ha, va="bottom" if up > 0 else "top", fontsize=9)
ax.set_xlim(24, 66); ax.set_ylim(-1.3, 1.8); ax.axis("off")
save(fig, 5)
