"""Figure 24.6: the hybrid's lead when one weight is halved or raised by half (options.txt sensitivity block)."""
import re
from _common import S, save, text
t = text("options")
rows = re.findall(r"^  ([a-z ]+?)\s+x0\.5\s+([+-][\d.]+) \(vs \w\)\s+x1\.5\s+([+-][\d.]+)", t, re.M)
base = float(re.search(r"lead of C over best other \(A\): ([\d.]+)", t).group(1))
rows = sorted(rows, key=lambda r: abs(float(r[2]) - float(r[1])))
fig, ax = S.figure(height=4.6)
for i, (d, lo, hi) in enumerate(rows):
    lo, hi = float(lo), float(hi)
    ax.plot([lo, hi], [i, i], color=S.PAL["grey"], lw=S.LW["emphasis"])
    ax.plot(lo, i, "o", color=S.PAL["coral"] if lo < 0 else S.PAL["slate"], ms=6)
    ax.plot(hi, i, "s", color=S.PAL["coral"] if hi < 0 else S.PAL["navy"], ms=6)
ax.axvline(0, color=S.ROLE["blocker"], lw=S.LW["control"]); ax.axvline(base, color=S.PAL["ink"], lw=0.75, ls="--")
ax.text(base + 0.1, len(rows) - 0.4, f"agreed weights {base:+.1f}", fontsize=10, color=S.PAL["ink"])
ax.text(0.1, -0.9, "below zero: new app wins", fontsize=10, color=S.PAL["ink"])
ax.set_yticks(range(len(rows)), [r[0] for r in rows]); ax.set_ylim(-1.3, len(rows) - 0.1)
ax.set_xlabel("lead of the hybrid, points (circle: weight x0.5, square: x1.5)")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 6, data="04-code/ch24/output/options.txt")
