"""Figure 41.7: the two Caldwell drills on one clock: detection, acknowledgment and the five verified runbook steps."""
from _common import S, save, text
def ev(name):
    out = []
    for l in text(name).splitlines():
        if len(l) > 5 and l[2] == ":" and l[:2].isdigit() and l[5] == " ":
            h, m = int(l[:2]), int(l[3:5]); out.append((h * 60 + m - 180, l[7:]))
    return out
fig, ax = S.figure(height=3.8)
for y, name, lab in ((1, "drill_1", "drill 1, day 176"), (0, "drill_2", "drill 2, day 183")):
    e = ev(name)
    ack = [t for t, s in e if "acknowledges" in s][0]; end = e[-1][0]
    ax.barh(y, ack, 0.42, color=S.ROLE["blocker"] if y else S.ROLE["evidence"], hatch="\\\\" if y else "xx", ec="white")
    ax.barh(y, end - ack, 0.42, left=ack, color=S.ROLE["approval"], ec="white")
    ax.text(end + 2, y, f"{end} min", va="center", fontsize=9)
    for t, s in e:
        if "vendor touch" in s:
            ax.plot(t, y + 0.3, marker="v", color=S.ROLE["blocker"], ms=8)
ax.axvline(60, color=S.PAL["ink"], ls="--", lw=0.75); ax.text(61, 1.45, "60-minute limit", fontsize=9)
ax.set_yticks([0, 1]); ax.set_yticklabels(["drill 2, day 183", "drill 1, day 176"])
ax.set_xlim(0, 170); ax.set_ylim(-0.5, 1.7); ax.set_xlabel("minutes after the fault (03:00)")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc=S.ROLE["blocker"], hatch="\\\\", ec="white", label="until a Caldwell person acknowledges"), Patch(fc=S.ROLE["approval"], label="runbook RB-03")], loc="lower right", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 7, data="04-code/ch41/output/drill_1.txt, drill_2.txt")
