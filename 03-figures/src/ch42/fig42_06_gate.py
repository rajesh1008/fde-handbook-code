"""Figure 42.6: the upgrade gate, extract-2026-04 against the incumbent, each dimension as a ratio to its floor
(deprecation.py dims; output/deprecation_v1.txt)."""
from _common import S, save, plt
dims = [("evaluation suite", 89.3, 87.2, 85.0, True), ("fully correct", 103, 76, 76, True),
        ("cost per document", 0.0358, 0.0358, 0.0400, False), ("p95 latency, accepted", 4.1, 3.8, 6.0, False)]
rat = lambda v, f, h: v / f if h else f / v
fig, ax = S.figure(height=4.0)
for i, (n, c, inc, f, h) in enumerate(dims):
    ax.barh(i - 0.2, rat(c, f, h), 0.38, color=S.ROLE["model"], label="candidate" if i == 0 else None)
    ax.barh(i + 0.2, rat(inc, f, h), 0.38, color=S.PAL["grey"], label="incumbent" if i == 0 else None)
ax.axvline(1.0, color=S.ROLE["blocker"], lw=S.LW["control"], ls="--"); ax.text(1.01, -0.55, "floor", fontsize=9)

ax.set_yticks(range(4)); ax.set_yticklabels([d[0] for d in dims]); ax.invert_yaxis()
ax.set_xlim(0.8, 1.75); ax.set_xlabel("ratio to floor (above 1 passes)"); ax.legend(fontsize=9, loc="upper right")
save(fig, 6, kind="plot", data="04-code/ch42/deprecation.py dims; output/deprecation_v1.txt")
