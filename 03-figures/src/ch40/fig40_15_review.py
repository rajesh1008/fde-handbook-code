"""Figure 40.15: how the twelve questions from Daniel Reyes's architects closed on day 184."""
from _common import S, save, text
rows = [l.split()[:2] for l in text("review").splitlines() if l.strip().startswith("Q")]
outs = [r[1] for r in rows]; assert len(outs) == 12 and outs.count("evidence") == 9
fig, ax = S.figure(height=3.7)
cats = [("evidence", "answered by evidence", "approval"), ("condition", "condition (A1, A2)", "data"), ("out", "out of scope", "evidence")]
for i, (k, lab, r) in enumerate(cats):
    n = outs.count(k)
    ax.barh(i, n, 0.55, color=S.ROLE[r]); ax.text(n + 0.15, i, str(n), va="center", fontsize=10)
ax.set_yticks(range(3)); ax.set_yticklabels([c[1] for c in cats]); ax.invert_yaxis(); ax.set_xlim(0, 10.5)
ax.set_xlabel("questions (12)"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 15, data="04-code/ch40/output/review.txt")
