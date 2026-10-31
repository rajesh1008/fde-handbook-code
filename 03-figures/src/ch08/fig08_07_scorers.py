"""Figure 8.7: the same outputs scored by three scorers: all fields against exact-check fields only."""
from _common import S, plt, save, quiet
import calibration as cal
r2 = cal.per_field(2); exact = [f for f, k, _ in r2 if k >= 0.8]
sets = [("round 1, all 14", cal.accuracy_by_scorer(1)), ("round 2, all 14", cal.accuracy_by_scorer(2)),
        ("round 2, 11 exact", cal.accuracy_by_scorer(2, exact))]
roles = ["model", "system", "evidence"]
fig, ax = S.figure(3.8)
for g, (name, acc) in enumerate(sets):
    for j, (s, v) in enumerate(acc.items()):
        x = g * 4 + j
        ax.bar(x, v * 100, color=S.ROLE[roles[j]], hatch=S.HATCH[roles[j]], edgecolor="white", width=0.8)
        ax.text(x, v * 100 + 0.25, f"{v * 100:.1f}", ha="center", fontsize=9)
    sp = (max(acc.values()) - min(acc.values())) * 100
    ax.text(g * 4 + 1, 95.0, f"spread {sp:.1f}", ha="center", fontsize=9)
ax.set_xticks([1, 5, 9]); ax.set_xticklabels([s[0] for s in sets], fontsize=9)
ax.set_ylim(86, 96.8); ax.set_ylabel("fields marked right (%)")
for j, n in enumerate(["Anne", "Tom", "adjuster B"]):
    ax.add_patch(plt.Rectangle((-0.5 + j * 2.6, 96.1), 0.4, 0.45, fc=S.ROLE[roles[j]], hatch=S.HATCH[roles[j]], ec="white"))
    ax.text(0.05 + j * 2.6, 96.3, n, fontsize=9, va="center")
ax.set_xlim(-0.7, 10.7)
save(fig, 7)
