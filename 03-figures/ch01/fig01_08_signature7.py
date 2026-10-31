"""Figure 1.8 (Signature 7, first state): fieldkit as it stands when the book opens, and where it grows."""
from _common import S, save, tbox
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 6.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 7.0); ax.axis("off")
ax.text(0.1, 6.75, "fieldkit 0.1.0 (exists now)", fontsize=10, weight="bold", color=S.PAL["ink"])
tbox(ax, 0.1, 5.2, 4.3, 1.25, "access.py\nAccessTracker, AccessRequest,\nLADDER (synthetic → sampled → shadowed → live)", role="evidence", fs=8.5)
tbox(ax, 5.6, 5.2, 4.3, 1.25, "readiness.py\nReadinessRegister, ReadinessResult", role="data", fs=8.5)
tbox(ax, 2.6, 3.65, 4.8, 1.05, "fixtures.py\nfour customers, their trackers, seeded claim sample", role="system", fs=8.5)
tbox(ax, 0.1, 2.25, 4.3, 0.95, "Chapter 1 lab: weeklog.py\ncalendar + tickets + commits → time allocation", role="approval", fs=8.5)
tbox(ax, 5.6, 2.25, 4.3, 0.95, "Chapter 15 lab: day47_status.py\naccess status on day 47", role="approval", fs=8.5)
for x1, y1, x2, y2 in [(3.6, 4.7, 2.6, 5.2), (6.4, 4.7, 7.4, 5.2), (2.25, 3.2, 3.6, 3.65), (7.75, 3.2, 6.4, 3.65)]:
    S.arrow(ax, x1, y1, x2, y2, color=S.PAL["ink"], ls="--")
ax.text(9.9, 3.9, "dashed arrow = imports", ha="right", fontsize=7.5, color=S.PAL["ink"])
ax.text(0.1, 1.75, "still to come (greyed: not built yet)", fontsize=10, weight="bold", color="#8A939E")
later = [("engagement repo\n(Ch 3, v0)", 0.1), ("scoping and\ndecision tree\n(Part II, v1.x)", 2.1),
         ("data and access\n(Part III, v2.x)", 4.1), ("evaluation and\nguardrails\n(Part IV, v3.x)", 6.1),
         ("gates, evidence pack,\nhand-over\n(Parts V-VI, v4-v5)", 8.1)]
for t, x in later:
    ax.add_patch(plt.Rectangle((x, 0.1), 1.8, 1.4, facecolor="#F3F4F6", edgecolor="#B8BFC8", ls="--", lw=1.2))
    ax.text(x + 0.9, 0.8, t, ha="center", va="center", fontsize=7.8, color="#6F7884")
save(fig, 8)
