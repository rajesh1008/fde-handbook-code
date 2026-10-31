"""Figure 17.6: day 64, denied connections in Caldwell's egress log per five minutes, by destination."""
import contextlib, io
from _common import S, save
with contextlib.redirect_stdout(io.StringIO()):
    import day64_deploy as d
mins = lambda t: (int(t[:2]) - 15) * 60 + int(t[3:5]) - 30
bins = list(range(0, 45, 5))
rows = {"api.model-provider.example:443": [0] * len(bins), "ingest.trace-vendor.example:443": [0] * len(bins)}
for r in d.log.query(action="DENY"):
    rows[r["dest"]][min(mins(r["t"]) // 5, len(bins) - 1)] += 1
fig, ax = S.figure(height=3.9)
a = rows["api.model-provider.example:443"]; b = rows["ingest.trace-vendor.example:443"]
ax.bar(bins, a, width=4.2, align="edge", color=S.ROLE["model"], edgecolor=S.PAL["ink"], lw=S.LW["data"], label=f"model provider ({sum(a)})")
ax.bar(bins, b, width=4.2, align="edge", bottom=a, color=S.ROLE["data"], edgecolor=S.PAL["ink"], lw=S.LW["data"], hatch="..", label=f"vendor tracing ({sum(b)})")
ax.set_xticks([0, 10, 20, 30, 40]); ax.set_xticklabels(["15:30", "15:40", "15:50", "16:00", "16:10"])
ax.set_ylabel("denied connections"); ax.set_xlabel("day 64, Eastern; run 2 at 17:05 had none")
ax.legend(loc="upper right"); ax.set_ylim(0, max(x + y for x, y in zip(a, b)) * 1.45)
save(fig, 6, data="04-code/ch17/day64_deploy.py (Caldwell egress log, stand-in)")
