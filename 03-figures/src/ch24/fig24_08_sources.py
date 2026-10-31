"""Figure 24.8: per-source latency, p50 and p95, against the 2.5 s per-source timeout (fanout.txt)."""
import re
from _common import S, save, text
t = text("fanout")
rows = re.findall(r"^  ([a-z-]+)\s+(\d+) /\s+(\d+)$", t, re.M)
to = int(re.search(r"timeout (\d+)", t).group(1))
fig, ax = S.figure(height=4.0)
rows = sorted(rows, key=lambda r: int(r[2]))
for i, (n, p50, p95) in enumerate(rows):
    hot = n == "claims-core"
    ax.barh(i, int(p95), color=S.TINT["blocker" if hot else "system"], edgecolor=S.ROLE["blocker" if hot else "system"], height=0.6)
    ax.barh(i, int(p50), color=S.ROLE["blocker" if hot else "system"], height=0.6)
    ax.text(int(p95) + 40, i, f"{int(p50):,} / {int(p95):,}", va="center", fontsize=10)
ax.axvline(to, color=S.PAL["ink"], ls="--", lw=S.LW["control"]); ax.text(to + 30, -0.75, f"timeout {to:,} ms", fontsize=10)
ax.set_yticks(range(len(rows)), [r[0] for r in rows]); ax.set_xlim(0, 3600); ax.set_ylim(-1.0, len(rows) - 0.4)
ax.set_xlabel("ms per source call: dark bar p50, light bar p95")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 8, data="04-code/ch24/output/fanout.txt")
