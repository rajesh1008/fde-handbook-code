"""Figure 29.10: the merge gate, from pull request to merge, hold or block (Listings 29.6 and 29.3)."""
from _common import S, save, blank
fig, ax = S.figure(height=4.2)
blank(ax, (0, 10), (0, 7))
S.box(ax, 0.2, 5.8, 2.2, 0.9, "pull request", role="data")
S.box(ax, 3.0, 5.8, 3.2, 0.9, "classify changed paths", role="system")
S.box(ax, 6.8, 5.8, 3.0, 0.9, "select layers", role="system")
S.arrow(ax, 2.4, 6.25, 3.0, 6.25); S.arrow(ax, 6.2, 6.25, 6.8, 6.25)
for i, (t, r) in enumerate((("L1 unit", "system"), ("L2 component", "model"), ("L3 integration", "data"))):
    x = 0.6 + i * 3.2
    S.box(ax, x, 3.9, 2.8, 0.9, t, role=r)
    S.arrow(ax, 8.3, 5.8, x + 1.4, 4.8, weight="data")
S.box(ax, 2.0, 2.3, 6.0, 0.9, "every metric, every slice: pass, fail, inconclusive", role="evidence", fs=9.5)
for i in range(3):
    S.arrow(ax, 2.0 + i * 3.2, 3.9, 5.0, 3.2, weight="data")
outs = [(0.2, "merge", "approval"), (3.5, "hold: data or sign-off", "evidence"), (6.8, "block: back to author", "blocker")]
for x, t, r in outs:
    S.box(ax, x, 0.3, 3.0, 1.0, t, role=r, fs=9.5)
    S.arrow(ax, 5.0, 2.3, x + 1.5, 1.3)
save(fig, 10, kind="diagram", data="fieldkit/pyramid.py MergeGate")
