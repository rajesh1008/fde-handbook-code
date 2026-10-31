"""Figure 26.6: agreement between two adjusters per field, calibration rounds 1 and 2 (Listing 26.3)."""
from _common import S, save, js
d = js("annotation")
fields = list(d["r1"])
fig, ax = S.figure(height=4.6)
for i, f in enumerate(fields):
    y = len(fields) - 1 - i
    k1, k2, line = d["r1"][f], d["r2"][f], d["lines"][f]
    ax.plot([k1, k2], [y, y], color=S.PAL["light"], lw=3, zorder=1)
    ax.scatter([k1], [y], color=S.ROLE["data"], s=45, zorder=2, label="round 1" if i == 0 else None)
    ax.scatter([k2], [y], color=S.ROLE["system"], marker="s", s=45, zorder=2, label="round 2" if i == 0 else None)
    ax.plot([line, line], [y - 0.4, y + 0.4], color=S.ROLE["blocker"], lw=2, zorder=3,
            label="line for the field" if i == 0 else None)
ax.set_yticks(range(len(fields)), fields[::-1], fontsize=9, family="monospace")
ax.set_xlim(-0.1, 1.05); ax.set_xlabel("Cohen's kappa, Whitfield vs adjuster B (40 documents)")
ax.set_ylim(-1.9, 9.6); ax.legend(loc="lower center", fontsize=9, ncol=3)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 6, data="04-code/ch26/output/annotation.json")
