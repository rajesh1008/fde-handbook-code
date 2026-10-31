"""Figure 7.4: the 66-question bank by category and audience."""
from _common import S, plt, save, quiet
import numpy as np
with quiet():
    import caldwell_bank as cb
b = cb.build(); cats = ["functional", "technical", "data", "identity", "audit"]
auds = ["data owner", "security lead", "model-risk officer", "operator"]
roles = ["system", "model", "data", "blocker", "approval"]
fig, ax = S.figure(3.8); left = np.zeros(len(auds))
for c, r in zip(cats, roles):
    v = np.array([sum(q.category == c for q in b.for_audience(a)) for a in auds])
    ax.barh(range(len(auds)), v, left=left, color=S.ROLE[r], hatch=S.HATCH[r], edgecolor="white", label=c)
    left += v
for i, t in enumerate(left):
    ax.text(t + 0.6, i, f"{int(t)}", va="center", fontsize=9)
ax.set_yticks(range(len(auds))); ax.set_yticklabels(auds, fontsize=9); ax.invert_yaxis()
ax.set_xlabel("questions"); ax.set_xlim(0, 46)
ax.legend(fontsize=9, loc="lower right", frameon=False)
save(fig, 4)
