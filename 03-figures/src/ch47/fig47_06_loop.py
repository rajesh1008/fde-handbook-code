"""Figure 47.6: the product loop: a field finding becomes a roadmap item only with code, a count and an owner."""
from _common import S, save, blank
fig, ax = S.figure(height=4.6); blank(ax, (0, 10), (0, 8))
B = [(0.2, 5.8, "field report\nwith code", "model"), (3.7, 5.8, "evidence\nscore", "evidence"),
     (7.2, 5.8, "monthly\ntriage", "approval"), (7.2, 0.6, "product\nrelease", "system"),
     (3.7, 0.6, "adopted at\nengagements", "data"), (0.2, 0.6, "playbook step\nretired", "cost")]
for x, y, t, r in B:
    S.box(ax, x, y, 2.6, 1.6, t, role=r, fs=10)
S.arrow(ax, 2.8, 6.6, 3.7, 6.6); S.arrow(ax, 6.3, 6.6, 7.2, 6.6); S.arrow(ax, 8.5, 5.8, 8.5, 2.2, weight="emphasis")
S.arrow(ax, 7.2, 1.4, 6.3, 1.4); S.arrow(ax, 3.7, 1.4, 2.8, 1.4); S.arrow(ax, 1.5, 2.2, 1.5, 5.8, ls="--")
S.label(ax, 4.0, 3.9, "no artifact: back to the pod", fs=9)
S.arrow(ax, 7.2, 6.0, 5.0, 4.4, ls="--")
save(fig, 6, kind="diagram", data="fieldkit/playbooks.py rank_reports, loop_metrics; 04-code/ch47/loop.py")
