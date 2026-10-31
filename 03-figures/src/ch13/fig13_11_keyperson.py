"""Key-person risk: who holds each capability, at Pennant and at Caldwell."""
from _common import S, save, plt
from cadence_data import HOLDINGS
fig, axes = S.figure(5.2, nrows=2)
for ax, (cust, h) in zip(axes, HOLDINGS.items()):
    people = sorted({p for hs in h.values() for p, _ in hs}, key=lambda p: (p == "lead FDE", p))
    caps = list(h)
    for x, p in enumerate(people):
        for y, c in enumerate(caps):
            held = any(pp == p for pp, _ in h[c])
            single = held and len(h[c]) == 1
            role = "blocker" if single else ("approval" if held else None)
            if role:
                ax.add_patch(plt.Rectangle((x - 0.4, y - 0.35), 0.8, 0.7, facecolor=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white"))
    ax.set_xticks(range(len(people))); ax.set_xticklabels([p.replace(" ", "\n") for p in people], fontsize=9)
    ax.set_yticks(range(len(caps))); ax.set_yticklabels(caps, fontsize=9)
    ax.set_xlim(-0.6, len(people) - 0.4); ax.set_ylim(len(caps) - 0.5, -0.5)
    ax.set_title(cust, fontsize=10, loc="left")
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(length=0)
fig.tight_layout()
save(fig, 11)
