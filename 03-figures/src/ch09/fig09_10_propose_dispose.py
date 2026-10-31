"""Figure 9.10: model proposes, code disposes. The loan-to-value service."""
from _common import S, save, blank
fig, ax = S.figure(4.2); blank(ax, (0, 10), (0, 6.4))
S.box(ax, 0.2, 4.6, 2.6, 1.2, "three\ndocuments", role="evidence", fs=10)
S.box(ax, 3.6, 4.6, 2.8, 1.2, "model proposes\ncited lines", role="model", fs=10)
S.box(ax, 7.2, 4.6, 2.6, 1.2, "code checks\neach citation", role="system", fs=10)
S.box(ax, 7.2, 2.4, 2.6, 1.2, "code computes\nLTV 73.0%", role="system", fs=10)
S.box(ax, 3.6, 2.4, 2.8, 1.2, "policy rule\n75% maximum", role="approval", fs=10)
S.box(ax, 0.2, 2.4, 2.6, 1.2, "decision with\nlineage", role="evidence", fs=10)
S.box(ax, 7.2, 0.3, 2.6, 1.2, "refuse to\nexceptions", role="blocker", fs=10)
S.arrow(ax, 2.8, 5.2, 3.6, 5.2); S.arrow(ax, 6.4, 5.2, 7.2, 5.2); S.arrow(ax, 8.5, 4.6, 8.5, 3.6)
S.arrow(ax, 7.2, 3.0, 6.4, 3.0); S.arrow(ax, 3.6, 3.0, 2.8, 3.0)
S.arrow(ax, 9.6, 4.6, 9.6, 1.5, ls="--"); S.label(ax, 9.65, 4.0, "fails", fs=9.5)
save(fig, 10, kind="diagram")
