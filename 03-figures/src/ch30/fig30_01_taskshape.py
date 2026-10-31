"""Figure 30.1: which task shapes are fine-tune candidates (diagram)."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9); blank(ax)
S.box(ax, 0.2, 4.3, 4.4, 1.3, "Closed label set\nclassify · extract · match", "data")
S.box(ax, 5.4, 4.3, 4.4, 1.3, "Open output\nsummary · synthesis", "model")
S.box(ax, 0.2, 2.3, 4.4, 1.3, "Labels exist, rules stable,\nvolume high", "evidence")
S.box(ax, 0.2, 0.3, 4.4, 1.2, "Run the fine-tune\nexperiment", "approval", lw=S.LW["emphasis"])
S.box(ax, 5.4, 0.3, 4.4, 1.2, "Prompt the frontier model", "model", lw=S.LW["emphasis"])
S.arrow(ax, 2.4, 4.3, 2.4, 3.6); S.arrow(ax, 2.4, 2.3, 2.4, 1.5); S.arrow(ax, 7.6, 4.3, 7.6, 1.5)
S.arrow(ax, 4.6, 2.95, 6.4, 1.5)
S.label(ax, 2.55, 1.8, "yes", fs=9); S.label(ax, 5.3, 2.4, "no", fs=9)
save(fig, 1, kind="diagram", data="Chapter 30 decision rule")
