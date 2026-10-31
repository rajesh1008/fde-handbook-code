"""Figure 42.11: the night of day 38, minute by minute (v0): calls rejected, documents reconciled, and the
timeline marks (output/drill_v0.txt)."""
import re
from _common import S, save, text, plt
rows = [l.split() for l in text("drill_v0").splitlines() if re.match(r"^\d\d:\d\d\s+\d", l)]
tm = lambda s: int(s[:2]) * 60 + int(s[3:]) - 120
x = [tm(r[0]) for r in rows]
fig, ax = S.figure(height=4.4)
ax.plot(x, [int(r[3]) for r in rows], color=S.ROLE["blocker"], lw=S.LW["emphasis"], label="calls rejected per minute")
ax.plot(x, [int(r[7]) for r in rows], color=S.ROLE["approval"], lw=S.LW["control"], label="documents reconciled")
marks = [(l.split()[0], l.split()[1]) for l in text("drill_v0").splitlines() if re.match(r"^  \d\d:\d\d", l)]
for t, k in [("02:10", "page"), ("02:31", "FDE"), ("02:58", "approval"), ("03:04", "rollback")]:
    ax.axvline(tm(t), color=S.PAL["grey"], lw=S.LW["data"], ls=":"); ax.text(tm(t) + 0.5, 0.97, k, fontsize=9, rotation=90, va="top", transform=ax.get_xaxis_transform())
ax.set_xticks([0, 10, 20, 30, 40, 50, 60]); ax.set_xticklabels(["02:00", "02:10", "02:20", "02:30", "02:40", "02:50", "03:00"])
ax.set_ylabel("count"); ax.legend(fontsize=9, loc="center right")
save(fig, 11, kind="plot", data="04-code/ch42/output/drill_v0.txt")
