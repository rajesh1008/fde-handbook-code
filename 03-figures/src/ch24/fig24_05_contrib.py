"""Figure 24.5: where the hybrid's 2.8-point lead over a new application comes from, per dimension (options.txt)."""
import re
from _common import S, save, text
t = text("options")
rows = re.findall(r"^  ([a-z ]+?)\s+C\s+([\d.]+)\s+A\s+([\d.]+)\s+diff\s+([+-][\d.]+)$", t, re.M)
tot = dict(re.findall(r"^  ([ABCD])\s+([\d.]+)\s{2}", t, re.M))
fig, ax = S.figure(height=4.6)
rows = sorted(rows, key=lambda r: float(r[3]))
for i, (d, c, a, diff) in enumerate(rows):
    v = float(diff)
    ax.barh(i, v, color=S.ROLE["approval"] if v > 0 else (S.ROLE["blocker"] if v < 0 else S.PAL["grey"]), height=0.6)
    ax.text(v + (0.2 if v >= 0 else -0.2), i, f"{v:+.1f}", va="center", ha="left" if v >= 0 else "right", fontsize=10, color=S.PAL["ink"])
ax.set_yticks(range(len(rows)), [r[0] for r in rows]); ax.axvline(0, color=S.PAL["ink"], lw=0.75)
ax.set_xlim(-5, 12); ax.set_xlabel("hybrid minus new application, weighted points")
ax.set_title(f"totals: C {tot['C']}, A {tot['A']}, B {tot['B']}, D {tot['D']}", fontsize=10, loc="left")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch24/output/options.txt")
