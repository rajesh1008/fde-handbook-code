"""Figure 25.13: missed errors per 1,000 proposals against the share escalated to two reviewers."""
import re
from _common import S, save, text
rows = [tuple(map(float, m)) for m in re.findall(r"^\s*(\d+)%\s+\d+\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)$", text("review_surface"), re.M)]
pct = [r[0] for r in rows]; missed = [r[3] for r in rows]; load = [r[1] for r in rows]
fig, ax = S.figure(height=3.7)
ax.plot(pct, missed, color=S.ROLE["blocker"], lw=2.0, marker="o", ms=4)
best = min(range(len(rows)), key=lambda i: missed[i])
ax.annotate(f"best: {pct[best]:.0f}%, {missed[best]:.1f}", xy=(pct[best], missed[best]), xytext=(pct[best] - 8, 45),
            fontsize=10, color=S.PAL["ink"], arrowprops=dict(arrowstyle="-", color=S.PAL["ink"], lw=0.75))
over = next(p for p, l in zip(pct, load) if l > 0.6)
ax.axvspan(over - 5, 100, color=S.TINT["cost"], zorder=0)
ax.text(over + 1, 100, "over a comfortable load", fontsize=10, color=S.PAL["ink"])
ax.set_xlabel("share of proposals escalated (%)"); ax.set_ylabel("missed errors per 1,000")
ax.set_ylim(0, 125); ax.spines[["top", "right"]].set_visible(False)
save(fig, 13, data="04-code/ch25/output/review_surface.txt (capacity model)")
