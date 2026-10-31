"""Figure 16.11: how wide the 95% interval on real accuracy is at 50, 100 and 200 documents (bootstrap)."""
import re
from _common import S, save, text
fig, ax = S.figure(height=3.9)
rows = [(int(a), float(b), float(c)) for a, b, c in re.findall(r"n=(\d+)\s+real accuracy 95% interval ([\d.]+)% to ([\d.]+)%", text("tryit_b"))]
for x, (n, lo, hi) in enumerate(rows):
    ax.plot([x, x], [lo, hi], color=S.ROLE["evidence"], lw=S.LW["emphasis"])
    ax.plot(x, (lo + hi) / 2, "o", color=S.ROLE["evidence"], ms=6)
    ax.text(x + 0.08, hi, f"{lo:.1f} to {hi:.1f}\n({hi - lo:.1f} points)", va="top", fontsize=9)
ax.axhline(94.1, color=S.ROLE["data"], ls="--", lw=S.LW["control"]); ax.text(-0.3, 92.6, "synthetic v1, 94.1", fontsize=9)
ax.set_xticks(range(len(rows))); ax.set_xticklabels([f"{n} documents" for n, _, _ in rows])
ax.set_xlim(-0.4, 2.8); ax.set_ylim(60, 97); ax.set_ylabel("real field accuracy (%)")
save(fig, 11, data="04-code/ch16/output/tryit_b.txt")
