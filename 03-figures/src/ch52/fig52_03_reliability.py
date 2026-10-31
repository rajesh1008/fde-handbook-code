"""Figure 52.3: the pinned model's confidence means what it says; gm-n2 states more than it delivers below 0.9."""
from _common import S, save, text
import re
pts = {}
for l in text("recalibrate").splitlines():
    m = re.match(r"\s+(gm-\S+)\s+(.*)", l)
    if m and "0.5-0.6" in l:
        pts[m.group(1)] = [int(x) for x in re.findall(r": (\d+)%", m.group(2))]
xs = [0.55, 0.65, 0.75, 0.85, 0.95]
fig, ax = S.figure(height=4.4)
ax.plot([0.5, 1.0], [50, 100], color=S.PAL["ink"], lw=S.LW["data"], ls=":")
ax.plot(xs, pts["gm-2026-05-14"], color=S.ROLE["evidence"], lw=S.LW["control"], marker="s", label="pin gm-2026-05-14")
ax.plot(xs, pts["gm-n2"], color=S.ROLE["blocker"], lw=S.LW["emphasis"], marker="o", ls="--", label="gm-n2, same calibrator")
ax.set_xlabel("Stated confidence"); ax.set_ylabel("Observed accuracy, %")
ax.set_ylim(20, 105); ax.legend(loc="lower right")
ax.text(0.505, 52, "perfect calibration", fontsize=9, rotation=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
save(fig, 3, data="04-code/ch52/output/recalibrate.txt")
