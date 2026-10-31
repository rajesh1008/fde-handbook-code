"""Figure 18.1: the path of one model call at Caldwell, and which parts Northlight owns."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6))
S.box(ax, 0.1, 3.3, 1.9, 1.2, "shadow runner\n(Northlight)", role="system", fs=10)
S.box(ax, 2.4, 3.3, 1.7, 1.2, "gateway\nadapter\n(fieldkit)", role="system", fs=10, lw=S.LW["emphasis"])
S.box(ax, 4.6, 2.2, 3.0, 3.1, "Caldwell gateway\n\nkey check\nallowlist\nquota\nsafety filter\nalias routing\nlogging", role="blocker", fs=10)
S.box(ax, 8.1, 3.3, 1.8, 1.2, "model\nproviders", role="model", fs=10)
S.box(ax, 2.4, 0.6, 1.7, 1.1, "secret store\n(Caldwell)", role="data", fs=10)
S.box(ax, 4.9, 0.6, 2.4, 1.1, "audit store\n(Caldwell)", role="evidence", fs=10)
S.arrow(ax, 2.0, 3.9, 2.4, 3.9); S.arrow(ax, 4.1, 3.9, 4.6, 3.9); S.arrow(ax, 7.6, 3.9, 8.1, 3.9)
S.arrow(ax, 3.25, 1.7, 3.25, 3.3); S.arrow(ax, 6.1, 2.2, 6.1, 1.7)
S.label(ax, 0.1, 5.65, "Northlight owns the two boxes on the left; Caldwell owns everything else", fs=10, color=S.PAL["slate"])
save(fig, 1, kind="diagram", data="chapter text (Caldwell call path)")
