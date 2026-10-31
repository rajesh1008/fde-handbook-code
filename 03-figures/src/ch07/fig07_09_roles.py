"""Figure 7.9: one bank, four audiences: questions per role and how many expected answers are guesses."""
from _common import S, plt, save, quiet
with quiet():
    import caldwell_bank as cb
b = cb.build(); auds = ["data owner", "security lead", "model-risk officer", "operator"]
G = ("vendor position", "proposed design", "decision required")
fig, ax = S.figure(3.8)
for i, a in enumerate(auds):
    qs = b.for_audience(a); g = sum(q.status in G for q in qs)
    ax.barh(i, len(qs) - g, color=S.ROLE["system"], hatch=S.HATCH["system"], edgecolor="white")
    ax.barh(i, g, left=len(qs) - g, color=S.ROLE["blocker"], hatch=S.HATCH["blocker"], edgecolor="white")
    ax.text(len(qs) + 0.6, i, f"{g} of {len(qs)} guessed", va="center", fontsize=9)
ax.set_yticks(range(4)); ax.set_yticklabels(auds, fontsize=9); ax.invert_yaxis()
ax.set_xlabel("questions (red hatch: vendor or proposed expected answer)"); ax.set_xlim(0, 52)
save(fig, 9)
