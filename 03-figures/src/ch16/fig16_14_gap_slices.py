"""Figure 16.14: the gap by slice, day 52 (synthetic v1) and day 58 (synthetic v2), same extractor v1."""
import re
from _common import S, save, text
t = text("gap_line").split("day 58")
def parse(b):
    out = {}
    for m in re.finditer(r"^\s{2}([a-z ,]+?)\s{2,}(none|[\d.]+%)\s+([\d.]+)%", b, re.M):
        s = m.group(2); out[m.group(1).strip()] = (None if s == "none" else float(s[:-1]), float(m.group(3)))
    return out
d52, d58 = parse(t[0]), parse(t[1])
fig, ax = S.figure(height=4.0)
sl = list(d52)
for i, s in enumerate(sl[::-1]):
    y = i
    real = d52[s][1]
    ax.plot(real, y, "s", color=S.ROLE["data"], ms=8, mec=S.PAL["ink"], mew=0.75, zorder=3)
    if d52[s][0] is not None:
        ax.plot(d52[s][0], y + 0.18, "o", color=S.ROLE["cost"], ms=7, mec=S.PAL["ink"], mew=0.75)
        ax.plot([real, d52[s][0]], [y + 0.18, y + 0.18], color=S.ROLE["cost"], lw=S.LW["data"])
    else:
        ax.text(real + 1.5, y + 0.18, "v1: untested", fontsize=9, va="center")
    ax.plot(d58[s][0], y - 0.18, "^", color=S.ROLE["evidence"], ms=7, mec=S.PAL["ink"], mew=0.75)
ax.set_yticks(range(len(sl))); ax.set_yticklabels(sl[::-1], fontsize=9.5)
ax.set_xlim(55, 102); ax.set_xlabel("field accuracy (%)")
ax.plot([], [], "s", color=S.ROLE["data"], mec=S.PAL["ink"], label="real 200")
ax.plot([], [], "o", color=S.ROLE["cost"], mec=S.PAL["ink"], label="synthetic v1, day 52")
ax.plot([], [], "^", color=S.ROLE["evidence"], mec=S.PAL["ink"], label="synthetic v2, day 58")
ax.legend(loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=3, frameon=False, fontsize=9, handletextpad=0.2, columnspacing=0.8)
save(fig, 14, data="04-code/ch16/output/gap_line.txt")
