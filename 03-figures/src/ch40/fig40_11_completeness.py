"""Figure 40.11: P1 pack completeness per day, as Caldwell's monitor computed it before and after the backfill."""
from _common import S, save, text, nums
before, after = text("monitor").split("AFTER BACKFILL")
pre = [nums(l) for l in before.splitlines() if l.strip().startswith("day")]
post = [nums(l) for l in after.split("MONITORS")[0].splitlines() if l.strip().startswith("day")]
assert pre[0][-1] == 0.0 and pre[-1][-1] == 100.0 and post[-1][0] == 215
fig, ax = S.figure(height=4.8)
d = [r[0] for r in post]; ver = [r[1] / 3.75 for r in post]; rec = [r[2] / 3.75 for r in post]
ax.bar(d, ver, 0.85, color=S.ROLE["approval"], label="verified at record time (after backfill)")
ax.bar(d, rec, 0.85, bottom=ver, color=S.ROLE["data"], hatch="..", label="reconstructed from history (after backfill)")
ax.plot([r[0] for r in pre], [r[-1] for r in pre], color=S.ROLE["blocker"], lw=S.LW["emphasis"], marker="o", ms=4, zorder=5, clip_on=False, label="complete, as of day 180 (v0 rules)")
ax.set_ylim(0, 105); ax.set_xlabel("engagement day decided"); ax.set_ylabel("decisions with a complete pack (%)")
ax.legend(fontsize=9, loc="lower center", bbox_to_anchor=(0.45, -0.52), ncol=1); ax.spines[["top", "right"]].set_visible(False)
save(fig, 11, data="04-code/ch40/output/monitor.txt")
