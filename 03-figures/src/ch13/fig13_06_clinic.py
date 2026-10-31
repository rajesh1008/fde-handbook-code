"""Greystone clinic outcomes by session: decisions, dated owner actions, items left with no outcome."""
from _common import S, save, plt
from cadence_data import GREYSTONE_CLINIC
days = sorted({r[3] for r in GREYSTONE_CLINIC})
cats = [("decision", "decision", "approval"), ("action", "dated owner action", "data"), (None, "no outcome", "blocker")]
fig, ax = S.figure(3.9)
bottom = [0] * len(days)
for key, lab, role in cats:
    vals = [sum(1 for r in GREYSTONE_CLINIC if r[3] == d and r[4] == key) for d in days]
    ax.bar(range(len(days)), vals, bottom=bottom, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white", width=0.6, label=lab)
    bottom = [b + v for b, v in zip(bottom, vals)]
ax.set_xticks(range(len(days))); ax.set_xticklabels([f"day {d}" for d in days])
ax.set_ylabel("items raised"); ax.set_ylim(0, 4.6); ax.set_yticks(range(0, 5))
ax.legend(frameon=False, fontsize=9, loc="upper left", ncol=3)
save(fig, 6)
