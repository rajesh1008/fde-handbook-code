"""Figure 6.7: what the exceptions were, most common first."""
from _common import S, plt, save
from collections import Counter
from caldwell_discovery import watched_documents
c = Counter(d.exception for d in watched_documents() if d.exception).most_common()
fig, ax = S.figure(3.8)
ks = [k for k, _ in c][::-1]; vs = [v for _, v in c][::-1]
ax.barh(ks, vs, color=S.TINT["blocker"], edgecolor=S.ROLE["blocker"], hatch="\\\\", lw=S.LW["data"])
for k, v in zip(ks, vs):
    ax.text(v + 0.4, k, str(v), va="center", fontsize=9.5)
ax.set_xlabel("watched documents (71 exceptions in 202)"); ax.set_xlim(0, 27)
save(fig, 7)
