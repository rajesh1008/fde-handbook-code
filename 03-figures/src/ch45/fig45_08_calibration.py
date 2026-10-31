"""Figure 45.8: interviewer offset from the panel median, by competency, before and after calibration."""
import sys
from _common import S, save, R, COMPS, text
sys.path.insert(0, str(R / "04-code/ch45"))
import world as W
from fieldkit.hiring import calibrate
assert "DRIFT Callum Reid on build: +0.83" in text("calibrate_before")
fig, ax = S.figure(height=4.4)
who = ("Callum Reid", "Sofia Brennan")
mk = dict(zip(who, ("s", "o")))
for wi, when in enumerate(("before", "after")):
    r = W.calibration(when)
    for k, w in enumerate(who):
        offs = [calibrate([x for x in r if x[2] == c])[w][0] for c in COMPS]
        ys = [i + (k - 0.5) * 0.3 for i in range(5)]
        ax.scatter(offs, ys, marker=mk[w], s=55, color=S.ROLE["blocker"] if when == "before" else S.ROLE["approval"],
                   label=f"{w}, {when}", zorder=3)
ax.axvspan(-0.5, 0.5, color="#EEEEEE", zorder=0); ax.text(0, -0.75, "within half a point", ha="center", fontsize=9.5)
ax.axvline(0, color=S.PAL["ink"], lw=S.LW["data"])
ax.set_yticks(range(5)); ax.set_yticklabels(COMPS); ax.invert_yaxis(); ax.set_ylim(4.6, -1.0)
ax.set_xlim(-1.1, 1.1); ax.set_xlabel("mean offset from the panel median (points)")
ax.legend(fontsize=9, loc="lower left"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 8, data="04-code/ch45/output/calibrate_before.txt, calibrate_after.txt; 04-code/ch45/world.py")
