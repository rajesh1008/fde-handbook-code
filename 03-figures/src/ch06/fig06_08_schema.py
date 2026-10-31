"""Figure 6.8: the discovery note, the log and the two reports it produces."""
from _common import S, plt, save, blank
fig, ax = S.figure(4.0); blank(ax, (0, 10), (0, 7))
S.box(ax, 0.2, 4.2, 3.0, 2.2, "note\nday, source, who\npath, question\nvalue, count", role="data", fs=9.5)
S.box(ax, 3.9, 4.6, 2.4, 1.4, "discovery log", role="system", fs=10)
S.box(ax, 7.0, 5.3, 2.8, 1.1, "coverage report", role="evidence", fs=9.5)
S.box(ax, 7.0, 3.6, 2.8, 1.1, "contradictions", role="blocker", fs=9.5)
S.box(ax, 3.9, 1.2, 2.4, 1.3, "resolution\nnamed person, day", role="approval", fs=9.5)
S.arrow(ax, 3.2, 5.3, 3.9, 5.3); S.arrow(ax, 6.3, 5.5, 7.0, 5.8); S.arrow(ax, 6.3, 5.0, 7.0, 4.2)
S.arrow(ax, 8.4, 3.6, 6.3, 1.9, weight="data"); S.arrow(ax, 5.1, 2.5, 5.1, 4.6, weight="data")
S.label(ax, 0.2, 3.5, "refused: identifiers, observations without a count", fs=9)
save(fig, 8, kind="diagram")
