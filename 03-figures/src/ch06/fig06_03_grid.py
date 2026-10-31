"""Figure 6.3: the five questions against the eleven paths on day 26."""
from _common import S, plt, save, SHORT
from matplotlib.patches import Rectangle
from caldwell_discovery import build_log, PATHS
from discovery import QUESTIONS
r = build_log().coverage(26)
fill = {"O": ("approval", ""), "a": ("data", ".."), "s": ("blocker", "\\\\"), ".": (None, "")}
fig, ax = S.figure(4.6)
qs = list(QUESTIONS)
for i, row in enumerate(r.rows):
    for j, q in enumerate(qs):
        m = row.marks[q]; role, h = fill[m]
        fc = S.TINT[role] if role else "white"; ec = S.ROLE[role] if role else S.PAL["light"]
        ax.add_patch(Rectangle((j, i), 0.92, 0.85, facecolor=fc, edgecolor=ec, hatch=h, lw=S.LW["data"]))
        ax.text(j + 0.46, i + 0.43, {"O": "seen", "a": "report", "s": "said", ".": ""}[m], ha="center", va="center",
                fontsize=9, color=S.PAL["ink"], bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none") if h else None)
ax.set_xlim(0, 5); ax.set_ylim(len(r.rows), 0)
ax.set_xticks([j + 0.46 for j in range(5)]); ax.set_xticklabels(["arrive", "touch", "decide", "except", "land"])
ax.xaxis.tick_top()
ax.set_yticks([i + 0.43 for i in range(len(r.rows))]); ax.set_yticklabels([SHORT[x.path] for x in r.rows])
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
save(fig, 3)
