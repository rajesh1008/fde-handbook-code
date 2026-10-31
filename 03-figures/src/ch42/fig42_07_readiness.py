"""Figure 42.7: Chapter 41 readiness re-run on production evidence, 0.40 to 0.30 to 0.80 (output/ownership.txt)."""
import re
from _common import S, save, text
rows = [re.match(r"\s*(\d+)\s+([\d.]+)(\*?)", l) for l in text("ownership").splitlines()]
pts = [(int(r.group(1)), float(r.group(2))) for r in rows if r and "." in r.group(2)]
fig, ax = S.figure(height=4.2)
x, y = zip(*pts); xs = list(x) + [90]; ys = list(y) + [y[-1]]
ax.step(xs, ys, where="post", color=S.ROLE["approval"], lw=S.LW["emphasis"])
ax.axhline(0.60, color=S.ROLE["blocker"], ls="--", lw=S.LW["control"]); ax.text(1, 0.62, "cap while a gate item is not done alone", fontsize=9)
ax.axhline(0.80, color=S.PAL["ink"], ls=":", lw=S.LW["control"]); ax.text(1, 0.82, "Live Stable line", fontsize=9)
for d, t in ((14, "sponsor leaves"), (43, "on-call moves"), (70, "drill alone")):
    v = dict(pts)[d]; ax.annotate(t, (d, v), (d + 2, v - 0.1), fontsize=9, arrowprops=dict(arrowstyle="-", color=S.PAL["grey"], lw=0.75))
ax.set_ylim(0, 1); ax.set_xlim(0, 92); ax.set_xlabel("production day"); ax.set_ylabel("readiness")
save(fig, 7, kind="plot", data="04-code/ch42/output/ownership.txt")
