"""Caldwell sprint 2 review: committed points by acceptance outcome."""
from _common import S, save, plt
from cadence_data import caldwell_sprint2
from fieldkit.cadence import review
rv = review("sprint 2", [i for i in caldwell_sprint2() if i.key != "C-06"], 56)
roles = {"accepted": "approval", "accepted with follow-up": "data", "not accepted": "blocker"}
fig, ax = S.figure(3.9)
y = 0
labels = []
for outcome, its in rv.outcomes.items():
    for i in its:
        ax.barh(y, i.points, color=S.ROLE[roles[outcome]], hatch=S.HATCH[roles[outcome]], edgecolor="white", height=0.6)
        ax.text(i.points + 0.15, y, f"{i.priority}  {outcome}", va="center", fontsize=9)
        labels.append(i.key); y += 1
ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels)
ax.set_xlim(0, 15); ax.set_xlabel("story points"); ax.invert_yaxis()
ax.text(14.8, 0.1, f"{rv.accepted_points} of {rv.committed} points accepted", ha="right", fontsize=10)
save(fig, 8)
