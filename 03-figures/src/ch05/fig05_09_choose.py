"""Figure 5.8: weighted home scores for three candidate profiles."""
from _common import S, save, plt, FIGSIZE, HOME_ROLE, HOME_NAME
from choose import PROFILES, score

profiles = dict(PROFILES)
profiles["production-minded\ncandidate (Try 3)"] = [0.20, 0.10, 0.10, 0.30, 0.10, 0.20]
fig, ax = plt.subplots(figsize=FIGSIZE)
w = 0.26
for j, k in enumerate(["vendor", "integrator", "lab"]):
    for i, (name, wts) in enumerate(profiles.items()):
        v = score(wts)[k]
        x = i + (j - 1) * w
        ax.bar(x, v, width=w * 0.95, color=S.ROLE[HOME_ROLE[k]], hatch=S.HATCH[HOME_ROLE[k]],
               edgecolor="white", label=HOME_NAME[k] if i == 0 else None)
        ax.text(x, v + 0.05, f"{v:.2f}", ha="center", fontsize=9)
ax.set_xticks(range(len(profiles))); ax.set_xticklabels(list(profiles), fontsize=9.5)
ax.set_ylim(0, 3); ax.set_ylabel("weighted score, 0 to 3")
ax.legend(loc="upper left", fontsize=9, frameon=True, fancybox=False, ncols=3)
save(fig, 9)
