"""Figure 17.2: retrieval under a narrow service identity, release under the user's delegation."""
from _common import S, save, blank
fig, ax = S.figure(height=4.0)
blank(ax, (0, 10), (0, 6))
S.box(ax, 0.1, 4.3, 2.1, 1.2, "adjuster\nsigned in", role="approval")
S.box(ax, 3.4, 4.3, 2.6, 1.2, "agent nl-assist\n15-minute delegation", role="system")
S.box(ax, 7.4, 4.3, 2.5, 1.2, "claims replica\nsvc-nl-claims-ro", role="data")
S.box(ax, 3.4, 1.0, 2.6, 1.3, "release gate\nrecheck each result", role="system", lw=S.LW["emphasis"])
S.box(ax, 7.4, 1.0, 2.5, 1.3, "claims-core\nauthorization", role="blocker")
S.box(ax, 0.1, 1.0, 2.1, 1.3, "results the\nadjuster may read", role="approval")
S.arrow(ax, 2.2, 4.9, 3.4, 4.9); S.arrow(ax, 6.0, 4.9, 7.4, 4.9)
S.arrow(ax, 4.7, 4.3, 4.7, 2.3); S.arrow(ax, 6.0, 1.65, 7.4, 1.65); S.arrow(ax, 3.4, 1.65, 2.2, 1.65)
S.label(ax, 6.1, 5.15, "retrieve", fs=9); S.label(ax, 6.1, 1.85, "ask, now", fs=9)
save(fig, 2, kind="diagram", data="chapter text; 04-code/ch17/obo_recheck.py")
