"""Figure 14.2: the question bank by room, and the claim status of each answer on day 19."""
from _common import S, save, plt
import question_bank as qb

labels = ["direct customer fact", "reconstructed from an artifact", "vendor position", "proposed design", "not answered"]
roles = ["approval", "evidence", "cost", "model", "blocker"]
rooms = ["Michael", "Sam"]
counts = []
for r in rooms:
    qs = [q for q in qb.BANK if q.room == r]
    row = [sum(1 for q in qs if q.status == s) for s in labels[:4]] + [sum(1 for q in qs if q.day_answered is None)]
    counts.append(row)
fig, ax = S.figure(3.8)
for i, row in enumerate(counts):
    left = 0
    for v, role in zip(row, roles):
        if v:
            ax.barh(i, v, left=left, height=0.5, color=S.TINT[role], edgecolor=S.ROLE[role], hatch=S.HATCH[role], lw=1.2)
            ax.text(left + v / 2, i, str(v), ha="center", va="center", fontsize=10,
                    bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
        left += v
ax.set_yticks([0, 1]); ax.set_yticklabels(["Michael Hart's room\n(clinical, 18)", "Sam Oakley's room\n(controls, 16)"], fontsize=9.5)
ax.set_ylim(1.5, -2.1); ax.set_xlim(0, 19); ax.set_xlabel("questions")
handles = [plt.Rectangle((0, 0), 1, 1, fc=S.TINT[r], ec=S.ROLE[r], hatch=S.HATCH[r]) for r in roles]
ax.legend(handles, labels, loc="upper left", ncol=2, fontsize=9, frameon=False)
save(fig, 2)
