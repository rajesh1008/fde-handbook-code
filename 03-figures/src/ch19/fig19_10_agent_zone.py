"""Figure 19.10: where a screen agent belongs, by how often the screen changes and what a wrong action costs."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4)
blank(ax, (-0.4, 10), (0, 7))
S.box(ax, 1.0, 3.6, 4.0, 2.8, "scripted steps,\nfingerprinted", role="system", fs=10.5)
S.box(ax, 5.2, 3.6, 4.0, 2.8, "agent reads,\nperson acts", role="model", fs=10.5)
S.box(ax, 1.0, 0.6, 4.0, 2.8, "scripted steps", role="approval", fs=10.5)
S.box(ax, 5.2, 0.6, 4.0, 2.8, "agent,\nreversible only", role="evidence", fs=10.5)
S.arrow(ax, 1.0, 0.3, 9.4, 0.3); S.label(ax, 6.0, -0.15, "screen changes more often", fs=10)
S.arrow(ax, 0.7, 0.6, 0.7, 6.6); S.label(ax, 0.05, 2.2, "cost of a wrong write", fs=10, rotation=90)
save(fig, 10, kind="diagram", data="Section 19.5 decision rule")
