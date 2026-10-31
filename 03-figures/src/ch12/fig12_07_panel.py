"""Figure 12.7: the sixty-question bank by group and rehearsal status, with the count the panel asked (panel_run.py)."""
from _common import S, plt, save, handles, hbar
from harbourline import panel, GROUPS
rows = panel()
roles = dict(proof="approval", rehearsed="evidence"); roles["not rehearsed"] = "blocker"
names = ["architecture", "security, data", "model risk", "delivery", "operations", "commercial, exit"]
fig, ax = S.figure(3.9)
for i, (g, *_r) in enumerate(GROUPS):
    y, left = len(GROUPS) - 1 - i, 0
    for st, r in roles.items():
        k = sum(x["group"] == g and x["status"] == st for x in rows)
        hbar(ax, y, left, k, r); left += k
    asked = sum(x["group"] == g and x["asked"] for x in rows)
    S.label(ax, left + 0.3, y, f"{asked} asked", fs=9.5, va="center")
ax.set_yticks(range(len(GROUPS))); ax.set_yticklabels(names[::-1])
ax.set_xlabel("questions in the bank"); ax.set_xlim(0, 17)
ax.legend(handles(roles.values()), ["with proof", "rehearsed", "not rehearsed"], loc="lower right")
save(fig, 7)
