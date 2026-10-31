"""Figure 12.2: outcomes of the 47-line platform-standards crosswalk by area, submitted draft (crosswalk_run.py)."""
from _common import S, plt, save, handles, hbar
from harbourline import standards, AREAS
from fieldkit.bid import STD_OUTCOMES
roles = ["system", "evidence", "blocker", "data"]
std = standards()
fig, ax = S.figure(3.9)
for i, (_, area, _n) in enumerate(AREAS):
    y, left = len(AREAS) - 1 - i, 0
    for o, r in zip(STD_OUTCOMES, roles):
        k = sum(s.area == area and s.outcome == o for s in std)
        if k:
            hbar(ax, y, left, k, r); left += k
ax.set_yticks(range(len(AREAS))); ax.set_yticklabels([a for _, a, _ in AREAS][::-1])
ax.set_xlabel("standards"); ax.set_xlim(0, 11)
ax.legend(handles(roles), ["comply", "configure", "deviation", "not applicable"], loc="lower right")
save(fig, 2)
