"""Figure 29.11: twelve seeded mutants, designed layer against catching layer, day 145 and day 152 (Listing 29.7)."""
from _common import S, save, js
d = js("control")
fig, axes = S.figure(height=4.4, ncols=2, sharey=True)
for ax, day in zip(axes, ("145", "152")):
    rows = d[day]
    for i, (mid, des, at, st) in enumerate(rows):
        ax.plot(des, i, "s", mfc="white", mec=S.PAL["ink"], ms=8)
        if at:
            col = S.ROLE["approval"] if st == "caught" else S.ROLE["data"]
            ax.plot(at, i, "o", color=col, ms=6)
            if at != des:
                ax.plot([des, at], [i, i], color=col, lw=S.LW["control"])
                S.label(ax, at + 0.2, i, "late", va="center", fs=9)
        else:
            ax.plot(5.7, i, "x", color=S.ROLE["blocker"], ms=8, mew=2)
            S.label(ax, 4.7, i, "escaped", va="center", ha="right", fs=9, weight="bold")
    ax.set_xticks([1, 2, 3, 4, 5], ["L1", "L2", "L3", "L4", "L5"], fontsize=9); ax.set_xlim(0.5, 6.1)
    ax.set_title(f"day {day}: {sum(r[3] == 'caught' for r in rows)} of 12 on time", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_yticks(range(12), [r[0] for r in d["145"]], fontsize=9); axes[0].invert_yaxis()
save(fig, 11, data="04-code/ch29/output/control.json")
