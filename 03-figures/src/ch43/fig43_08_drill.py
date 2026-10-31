"""Figure 43.8: the exit drill on MS-RB-01, v0 and v1, minute by minute from 02:00. Data: drill_v0.txt, drill_v1.txt."""
import re
from _common import S, save, text
fig, ax = S.figure(height=3.8)
for row, v in ((1, "v0"), (0, "v1")):
    t0 = 120
    for line in text(f"drill_{v}").splitlines():
        m = re.match(r"(\d\d):(\d\d)\s+step (\d): (.*)", line)
        if not m:
            continue
        t = int(m.group(1)) * 60 + int(m.group(2))
        what = m.group(4)
        role = "blocker" if what.startswith("blocked") else "cost" if what.startswith("workaround") else "approval"
        if t > t0:
            S.box(ax, t0, row + 0.15, t - t0, 0.7, "", role=role)
        elif role == "blocker":
            ax.plot([t, t], [row + 0.1, row + 0.9], color=S.ROLE["blocker"], lw=S.LW["emphasis"])
            ax.text(t + 2, row + 0.5, "blocked: vendor bastion", fontsize=9, va="center")
        t0 = max(t0, t)
ax.axvline(210, color=S.PAL["ink"], lw=S.LW["control"], ls="--"); ax.text(206, 1.95, "03:30 deadline", fontsize=9, ha="right")
ax.set_xlim(115, 215); ax.set_ylim(-0.1, 2.1)
ax.set_xticks([120, 150, 180, 210]); ax.set_xticklabels(["02:00", "02:30", "03:00", "03:30"])
ax.set_yticks([0.5, 1.5]); ax.set_yticklabels(["v1", "v0"])
save(fig, 8, data="04-code/ch43/output/drill_v0.txt, drill_v1.txt")
