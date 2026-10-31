"""Figure 6.5: days from arrival to a claim record, by path, from the watched documents."""
from _common import S, plt, save, SHORT
from caldwell_discovery import watched_documents, PATHS
docs = watched_documents()
fig, ax = S.figure(4.2)
ps = [p for p in PATHS if any(d.path == p.pid for d in docs)]
for i, p in enumerate(ps):
    lags = [d.lag_days for d in docs if d.path == p.pid]
    r = "system" if p.documented else "data"
    ax.scatter(lags, [i] * len(lags), s=14, color=S.ROLE[r], marker="o" if p.documented else "^", alpha=1, zorder=2)
    ax.plot([sum(lags) / len(lags)] * 2, [i - 0.35, i + 0.35], color=S.PAL["ink"], lw=S.LW["emphasis"], zorder=3)
ax.set_yticks(range(len(ps))); ax.set_yticklabels([SHORT[p.pid] for p in ps]); ax.invert_yaxis()
ax.set_xlabel("days from arrival to claim record (bar: mean)")
ax.axvline(0, color=S.PAL["grey"], lw=S.LW["data"], ls="--")
ax.text(0.1, -0.8, "procedure: same day", fontsize=9, color=S.PAL["ink"])
save(fig, 5)
