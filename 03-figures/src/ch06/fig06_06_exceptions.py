"""Figure 6.6: exceptions are a third of the documents and two thirds of the minutes."""
from _common import S, plt, save, SHORT
from caldwell_discovery import watched_documents, PATHS
docs = watched_documents()
fig, ax = S.figure(4.2)
ps = [p for p in PATHS if sum(d.path == p.pid for d in docs) >= 5]
for i, p in enumerate(ps):
    ds = [d for d in docs if d.path == p.pid]
    a = 100 * sum(1 for d in ds if d.exception) / len(ds)
    b = 100 * sum(d.work_min for d in ds if d.exception) / sum(d.work_min for d in ds)
    ax.plot([a, b], [i, i], color=S.PAL["light"], lw=S.LW["emphasis"], zorder=1)
    ax.scatter([a], [i], color=S.ROLE["evidence"], marker="o", s=45, zorder=3)
    ax.scatter([b], [i], color=S.ROLE["blocker"], marker="s", s=45, zorder=3)
ax.set_yticks(range(len(ps))); ax.set_yticklabels([SHORT[p.pid] for p in ps]); ax.invert_yaxis()
ax.set_xlim(-5, 105); ax.set_xlabel("percent of watched documents (circle) and of minutes (square)")
ax.scatter([], [], color=S.ROLE["evidence"], marker="o", label="share of documents")
ax.scatter([], [], color=S.ROLE["blocker"], marker="s", label="share of minutes")
ax.legend(frameon=False, fontsize=9, loc="upper right")
save(fig, 6)
