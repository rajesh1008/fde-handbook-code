"""Figure 12.1: who owns each of Harbourline's 200 RFP questions, by section (triage_run.py)."""
from _common import S, plt, save, handles, hbar
from fieldkit.bid import triage
from harbourline import questions, SECTIONS
_, by, _ = triage(questions())
names = ["A company", "B commercial", "C legal", "D architecture", "E security", "F model risk", "G delivery",
         "H operations", "I exit"]
roles = dict(engineering="system", joint="evidence", sales="cost")
fig, ax = S.figure(4.0)
for i, (sec, *_r) in enumerate(SECTIONS):
    y, left = len(SECTIONS) - 1 - i, 0
    for o in ("engineering", "joint", "sales"):
        hbar(ax, y, left, by[sec][o], roles[o]); left += by[sec][o]
ax.set_yticks(range(len(SECTIONS))); ax.set_yticklabels(names[::-1])
ax.set_xlabel("questions"); ax.set_xlim(0, 32)
ax.legend(handles(roles.values()), ["engineering", "joint", "sales"], loc="lower right")
save(fig, 1)
