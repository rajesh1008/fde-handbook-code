"""Figure 21.3: document volume by layout on the 2,000-document sample, ranked, with the cumulative share."""
import sys
from _common import S, save, R
sys.path.insert(0, str(R / "04-code/ch21"))
from pennant import volumes
v = sorted(volumes(), reverse=True)
cum, run = [], 0
for x in v:
    run += x; cum.append(100 * run / sum(v))
fig, ax = S.figure(height=3.9)
ax.bar(range(1, 42), v, color=[S.ROLE["system"] if i < 12 else S.PAL["grey"] for i in range(41)], width=0.8)
ax.set_xlabel("layout, ranked by volume"); ax.set_ylabel("documents")
ax2 = ax.twinx(); ax2.plot(range(1, 42), cum, color=S.ROLE["data"], lw=S.LW["control"])
ax2.set_ylim(0, 105); ax2.set_ylabel("cumulative share (%)")
ax2.axvline(12.5, color=S.PAL["ink"], lw=S.LW["data"], ls="--")
ax2.text(13.2, cum[11] - 9, f"top 12 layouts: {cum[11]:.0f}%", fontsize=10, color=S.PAL["ink"])
ax2.text(26, 60, "29 layouts share the rest", fontsize=10, color=S.PAL["ink"])
save(fig, 3, data="04-code/ch21/pennant.py volumes(); matches output/variability.txt")
