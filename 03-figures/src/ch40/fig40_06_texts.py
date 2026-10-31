"""Figure 40.6: calls per day by the prompt text actually sent; every v0 record named text A."""
from _common import S, save, text, nums
rows = [nums(l) for l in text("rerun").split("TOKEN GAP")[0].splitlines() if l.strip().startswith("day")]
days = [r[0] for r in rows]; a = [r[1] for r in rows]; b = [r[2] for r in rows]
assert days[0] == 158 and a[8] == 34 and b[8] == 341
fig, ax = S.figure(height=4.2)
ax.bar(days, a, 0.8, color=S.ROLE["system"], hatch="//", label="text A (in the commit)")
ax.bar(days, b, 0.8, bottom=a, color=S.ROLE["blocker"], label="text B (hotfix, parameter store)")
ax.axvline(165.6, color=S.PAL["ink"], lw=S.LW["control"], ls="--")
S.label(ax, 166.0, 392, "hotfix day 166, 02:10", fs=9.5)
ax.set_ylim(0, 440); ax.set_xlabel("engagement day"); ax.set_ylabel("calls per day")
ax.legend(fontsize=9.5, loc="lower center", bbox_to_anchor=(0.45, -0.42), ncol=2); ax.spines[["top", "right"]].set_visible(False)
save(fig, 6, data="04-code/ch40/output/rerun.txt")
