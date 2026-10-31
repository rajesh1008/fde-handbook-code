"""Figure 5.3: what one more month before production does to the employer's P&L, by home."""
from _common import S, save, plt, FIGSIZE
import economics as E

rows = E.extra_month_split()
names = ["vendor, fixed fee\n(Caldwell)", "vendor, subscription\nat production (Greystone)",
         "integrator, T&M", "model lab\n+ partner"]
fig, ax = plt.subplots(figsize=FIGSIZE)
for i, r in enumerate(rows):
    v = r.employer_net / 1e3
    role = "approval" if v > 0 else "blocker"
    ax.barh(i, v, height=0.55, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white")
    ax.text(v + (6 if v > 0 else -6), i, f"{'+' if v > 0 else '-'}${abs(v):,.1f}k", va="center",
            ha="left" if v > 0 else "right", fontsize=9.5)
ax.axvline(0, color=S.PAL["ink"], lw=1)
ax.set_yticks(range(len(rows))); ax.set_yticklabels(names, fontsize=9.5); 
ax.set_xlim(-300, 80); ax.set_xlabel("employer net for one more month, thousands of US dollars")
ax.set_ylim(3.5, -1.0)
ax.text(-295, -0.75, "integrator: the only home where delay earns", fontsize=9, color=S.PAL["ink"])
save(fig, 3)
