"""Figure 19.9: end-to-end success of a screen task as steps grow, at three per-step success rates."""
from _common import S, save
fig, ax = S.figure(height=4.2)
n = list(range(1, 31))
for p, r in [(0.99, "system"), (0.97, "model"), (0.95, "blocker")]:
    ax.plot(n, [p ** k for k in n], color=S.ROLE[r], lw=S.LW["control"], label=f"per step {p:.2f}")
ax.axvline(14, color=S.PAL["grey"], lw=0.75, ls="--")
ax.text(14.4, 0.12, "first notice:\n14 steps", fontsize=9.5)
ax.set_xlabel("steps in the task"); ax.set_ylabel("end-to-end success"); ax.set_ylim(0, 1.02)
ax.legend(loc="lower left", fontsize=9.5, edgecolor=S.PAL["light"])
save(fig, 9, data="04-code/ch19/output/screen_reliability.txt (p**n)")
