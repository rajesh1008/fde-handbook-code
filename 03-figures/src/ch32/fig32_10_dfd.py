"""Figure 32.10: the document agent's data flows and trust boundaries, with the undeclared flow."""
from matplotlib.patches import Rectangle
from _common import S, save, blank
fig, ax = S.figure(height=5.2); blank(ax, (0, 10), (0, 9.5))
def zone(x, y, w, h, t):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=S.PAL["grey"], lw=1.5, ls="--")); S.label(ax, x + 0.1, y + h + 0.1, t, fs=9)
zone(1.9, 0.4, 5.3, 8.3, "Greystone tenant"); zone(7.5, 4.6, 2.4, 4.1, "provider"); zone(7.5, 0.4, 2.4, 2.6, "EHR network")
S.box(ax, 0.1, 7.0, 1.5, 1.0, "clinics", role="data")
S.box(ax, 2.1, 7.0, 1.6, 1.0, "intake", role="system"); S.box(ax, 4.0, 7.0, 1.6, 1.0, "store", role="data")
S.box(ax, 5.8, 7.0, 1.3, 1.0, "index", role="data")
S.box(ax, 3.4, 4.6, 2.2, 1.2, "orchestrator", role="model")
S.box(ax, 7.7, 7.0, 2.0, 1.0, "model", role="model")
S.box(ax, 7.7, 4.9, 2.0, 1.2, "diagnostics", role="blocker", ls="--", lw=S.LW["emphasis"])
S.box(ax, 7.7, 0.8, 2.0, 1.0, "EHR", role="data")
S.box(ax, 2.1, 2.4, 1.6, 1.0, "queue", role="system"); S.box(ax, 4.0, 2.4, 1.4, 1.0, "audit", role="evidence")
S.box(ax, 5.6, 2.4, 1.4, 1.0, "traces", role="evidence"); S.box(ax, 5.4, 0.7, 1.6, 1.0, "connector", role="system")
S.box(ax, 2.1, 0.7, 1.6, 1.0, "coordinator", role="approval")
a = S.arrow
a(ax, 1.6, 7.5, 2.1, 7.5); a(ax, 3.7, 7.5, 4.0, 7.5); a(ax, 5.6, 7.5, 5.8, 7.5)
a(ax, 5.0, 5.8, 6.2, 7.0); a(ax, 5.6, 5.5, 7.7, 7.3, weight="emphasis"); a(ax, 5.6, 5.0, 7.7, 5.4, color=S.ROLE["blocker"], ls="--", weight="emphasis")
a(ax, 3.8, 4.6, 2.9, 3.4); a(ax, 4.5, 4.6, 4.7, 3.4); a(ax, 5.2, 4.6, 6.2, 3.4); a(ax, 5.2, 4.6, 6.0, 1.7)
a(ax, 7.0, 1.2, 7.7, 1.2, weight="emphasis"); a(ax, 2.9, 1.7, 2.9, 2.4)
S.label(ax, 6.0, 4.55, "undeclared", fs=9)
save(fig, 10, kind="diagram", data="04-code/ch32/world.py FLOWS, OBSERVED; output/dataflows.txt")
