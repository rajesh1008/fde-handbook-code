"""Figure 9.1: demo agent against the deterministic-first pipeline, cost per document and median latency."""
from _common import S, save, plt, weighted
import random, costs as K
from intake_paths import walk_paths
demo, new, _ = weighted()
rng = random.Random(9); ld, ln = [], []
for row, _, c, _ in walk_paths():
    for _ in range(max(1, row[2] // 100)):
        ln.append(K.pipeline_latency(c, rng)[1]); ld.append(K.demo_latency(rng)[1])
fig, (a, b) = S.figure(3.8, ncols=2)
for ax, vals, fmt, yl in ((a, [demo * 100, new * 100], "{:.1f}¢", "cents per document"),
                          (b, [K.pct(ld, .5), K.pct(ln, .5)], "{:.1f} s", "median seconds per document")):
    ax.bar([0, 1], vals, width=0.6, color=[S.ROLE["cost"], S.ROLE["system"]], hatch=[S.HATCH["cost"], S.HATCH["system"]], edgecolor="white")
    for i, v in enumerate(vals): ax.text(i, v * 1.03, fmt.format(v), ha="center", fontsize=10)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["demo agent", "pipeline"], fontsize=10); ax.set_ylabel(yl, fontsize=10)
    ax.set_ylim(0, max(vals) * 1.22)
a.set_title(f"cost falls {1 - new / demo:.0%}", fontsize=10.5); b.set_title("wait falls by two thirds", fontsize=10.5)
save(fig, 1)
