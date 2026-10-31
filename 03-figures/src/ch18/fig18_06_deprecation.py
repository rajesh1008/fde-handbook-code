"""Figure 18.6: days left on the v1 endpoint as the register saw it, with the alert levels and day 100."""
import re
from _common import S, save, text
fig, ax = S.figure(height=3.9)
rows = [(int(d), int(n)) for d, n in re.findall(r"day (\d+) \w+ 10:00.*?register: (-?\d+) days left", text("deprecation"))]
xs, ys = zip(*rows)
ax.plot(xs, ys, "o-", color=S.ROLE["blocker"], lw=S.LW["emphasis"])
for x, y in rows:
    ax.text(x + 0.8, y + 1.5, f"day {x}: {y}", fontsize=9)
ax.axhline(30, color=S.PAL["amber"], ls="--", lw=S.LW["control"]); ax.text(70, 31, "warn at 30 days", fontsize=9)
ax.axhline(7, color=S.PAL["coral"], ls="--", lw=S.LW["control"]); ax.text(70, 8, "page at 7 days", fontsize=9)
ax.axvline(100, color=S.PAL["slate"], ls=":", lw=S.LW["control"]); ax.text(100.5, 42, "shadow\nstarts", fontsize=9)
ax.set_xlabel("engagement day"); ax.set_ylabel("days until Sunset")
ax.set_xlim(66, 124); ax.set_ylim(-5, 55)
save(fig, 6, data="04-code/ch18/output/deprecation.txt")
