"""Figure 9.4: Caldwell's eleven intake paths against the twelve steps; blank where a path skips a step."""
from _common import S, save, plt, CLASS_ROLE, CLASS_NAME, handles
from fieldkit.autonomy import classify
import pipelines as pl
from intake_paths import PATHS, steps_for
fig, ax = S.figure(4.8)
for r, row in enumerate(PATHS):
    have = {s.n for s in steps_for(row[0])}
    for c, s in enumerate(pl.CALDWELL):
        if s.n in have:
            k = CLASS_ROLE[classify(s)]
            ax.add_patch(plt.Rectangle((c, r), 0.92, 0.85, fc=S.ROLE[k], hatch=S.HATCH[k], ec="white"))
        else:
            ax.add_patch(plt.Rectangle((c, r), 0.92, 0.85, fc=S.PAL["mist"], ec=S.PAL["light"]))
    if row[0] == "P09":
        ax.text(12.15, r + 0.42, "refused: no owner", fontsize=9, va="center", color=S.PAL["ink"], weight="bold")
ax.set_xlim(0, 15.2); ax.set_ylim(len(PATHS) + 0.2, -2.4)
ax.set_xticks([c + 0.46 for c in range(12)]); ax.set_xticklabels([s.n[1:] for s in pl.CALDWELL], fontsize=9)
ax.set_yticks([r + 0.42 for r in range(len(PATHS))]); ax.set_yticklabels([f"{p[0]} {p[2]:,}" for p in PATHS], fontsize=9)
for sp in ax.spines.values(): sp.set_visible(False)
ax.tick_params(length=0); ax.set_xlabel("pipeline step (C01 to C12)", fontsize=9.5)
ax.legend(handles(), CLASS_NAME, loc="upper left", ncol=2, fontsize=9, frameon=False, bbox_to_anchor=(0, 1.0))
save(fig, 4)
