"""Figure 9.13: latency per document, median and 95th percentile, by class and end to end."""
from _common import S, save, plt
import random, costs as K
from intake_paths import walk_paths
rng = random.Random(9); cls = {k: [] for k in ("det", "rules", "small", "frontier")}; ln, ld = [], []
for row, _, c, _ in walk_paths():
    for _ in range(max(1, row[2] // 100)):
        b, t = K.pipeline_latency(c, rng); ln.append(t); ld.append(K.demo_latency(rng)[1])
        for k in b:
            if b[k]: cls[k].append(b[k])
rows = [("rules", cls["rules"], "approval"), ("deterministic", cls["det"], "system"), ("small model", cls["small"], "data"),
        ("frontier model", cls["frontier"], "model"), ("pipeline total", ln, "evidence"), ("demo agent", ld, "cost")]
fig, ax = S.figure(4.0)
for i, (lab, xs, r) in enumerate(rows):
    p50, p95 = K.pct(xs, .5), K.pct(xs, .95)
    ax.barh(i, p95, height=0.55, color=S.TINT[r], edgecolor=S.ROLE[r], lw=1.2)
    ax.barh(i, p50, height=0.55, color=S.ROLE[r], hatch=S.HATCH[r], edgecolor="white")
    ax.text(p95 * 1.15, i, f"{p50:.2f} / {p95:.2f} s" if p95 < 1 else f"{p50:.1f} / {p95:.1f} s", va="center", fontsize=9.5)
ax.set_xscale("log"); ax.set_xlim(0.01, 200); ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=9.5)
ax.invert_yaxis(); ax.set_xlabel("seconds per document (log scale); dark = median, light = 95th percentile")
save(fig, 13)
