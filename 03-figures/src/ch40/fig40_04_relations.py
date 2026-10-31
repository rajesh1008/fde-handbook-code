"""Figure 40.4: an event says that something happened; evidence carries four relations around the decision record."""
from _common import S, save, blank
fig, ax = S.figure(height=4.6); blank(ax, (0, 10), (0, 9))
S.box(ax, 3.3, 3.7, 3.4, 1.6, "decision\nrecord", role="model", fs=11)
rel = [(0.2, 6.6, "provenance:\nwhich document"), (6.0, 6.6, "derivation:\nwhich steps"),
       (0.2, 0.6, "authority:\nwho may act"), (6.0, 0.6, "validity:\nwhich version, when")]
for x, y, t in rel:
    S.box(ax, x, y, 3.8, 1.7, t, role="evidence", fs=10)
S.arrow(ax, 2.1, 6.6, 3.6, 5.3); S.arrow(ax, 7.9, 6.6, 6.4, 5.3)
S.arrow(ax, 2.1, 2.3, 3.6, 3.7); S.arrow(ax, 7.9, 2.3, 6.4, 3.7)
save(fig, 4, kind="diagram", data="Section 40.2; evidence model in 04-code/ch40/pack.py")
