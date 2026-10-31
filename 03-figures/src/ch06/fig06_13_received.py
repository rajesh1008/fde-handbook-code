"""Figure 6.13: share of watched documents whose recorded received date is later than arrival."""
from _common import S, plt, save, SHORT
from caldwell_discovery import watched_documents, PATHS
docs = watched_documents()
ps = [p for p in PATHS if sum(d.path == p.pid for d in docs) >= 5]
fig, ax = S.figure(3.8)
vals = [100 * sum(d.lag_days >= 0.5 for d in docs if d.path == p.pid) / sum(d.path == p.pid for d in docs) for p in ps]
for i, (p, v) in enumerate(zip(ps, vals)):
    r = "system" if p.documented else "data"
    ax.bar(i, v, color=S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r], lw=S.LW["data"])
    ax.text(i, v + 2, f"{v:.0f}%", ha="center", fontsize=9)
ax.set_xticks(range(len(ps))); ax.set_xticklabels([SHORT[p.pid].replace(" ", "\n", 1) for p in ps], fontsize=9)
ax.set_ylim(0, 112); ax.set_ylabel("percent of watched documents")
save(fig, 13)
