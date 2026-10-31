"""Figure 5.7: the customer's five questions, risk by home."""
from _common import S, save, plt, FIGSIZE
from customer_view import QUESTIONS, totals

keys = ["vendor", "integrator", "lab"]
MK = {0: ("o", "approval", "low"), 1: ("s", "data", "medium"), 2: ("^", "blocker", "high")}
fig, ax = plt.subplots(figsize=FIGSIZE)
for i, (q, row) in enumerate(QUESTIONS):
    for j, k in enumerate(keys):
        r = row[k][1]
        m, role, _ = MK[r]
        ax.scatter(j, i, s=260, marker=m, color=S.ROLE[role], edgecolor=S.PAL["ink"], zorder=3)
        ax.text(j + 0.16, i, MK[r][2], va="center", fontsize=9)
t = totals()
ax.set_xticks(range(3)); ax.set_xticklabels([f"product vendor\nrisk {t['vendor']}/10",
                                              f"integrator\nrisk {t['integrator']}/10",
                                              f"model lab\nrisk {t['lab']}/10"], fontsize=9.5)
ax.set_yticks(range(len(QUESTIONS))); ax.set_yticklabels([q for q, _ in QUESTIONS], fontsize=9.5)
ax.set_xlim(-0.4, 2.7); ax.set_ylim(len(QUESTIONS) - 0.5, -0.5)
ax.grid(False)
save(fig, 6)
