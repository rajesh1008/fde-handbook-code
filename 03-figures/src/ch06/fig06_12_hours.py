"""Figure 6.12: hands-on hours a month by path."""
from _common import S, plt, save, SHORT
from caldwell_discovery import watched_documents, PATHS
docs = watched_documents(); rows = []
for p in PATHS:
    ds = [d for d in docs if d.path == p.pid]
    mpd = sum(d.work_min for d in ds) / len(ds) if ds else p.work_min * (1 - p.exc_rate) + p.exc_min * p.exc_rate
    rows.append((p, p.volume * mpd / 60))
rows.sort(key=lambda r: r[1])
fig, ax = S.figure(4.2)
for i, (p, h) in enumerate(rows):
    ax.barh(i, h, color=S.TINT["cost"], edgecolor=S.ROLE["cost"], hatch="--" if p.documented else "", lw=S.LW["data"])
    ax.text(h + 8, i, f"{h:,.0f}", va="center", fontsize=9)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([SHORT[p.pid] for p, _ in rows])
ax.set_xlabel("hands-on hours a month (dashed fill: in the procedure)"); ax.set_xlim(0, 800)
save(fig, 12)
