"""Figure 10.4: the estimation model: inventory lines, lint, simulation, the customer page."""
from _common import S, plt, save, clean
fig, ax = S.figure(4.2); clean(ax)
S.box(ax, 0.2, 4.6, 3.0, 1.6, "systems inventory\none line per piece of work", role="data")
S.box(ax, 3.7, 4.6, 2.8, 1.6, "line: source, hours\nlow, likely, high", role="evidence")
S.box(ax, 7.0, 4.6, 2.8, 1.6, "fact underneath:\nstatus, owner", role="evidence")
S.box(ax, 0.2, 1.0, 3.0, 1.6, "lint: unpriced\nassumption refused", role="blocker")
S.box(ax, 3.7, 1.0, 2.8, 1.6, "seeded simulation\nP10, P50, P90", role="model")
S.box(ax, 7.0, 1.0, 2.8, 1.6, "customer page:\nrange, drivers, owners", role="approval", lw=S.LW["emphasis"])
S.arrow(ax, 3.2, 5.4, 3.7, 5.4); S.arrow(ax, 6.5, 5.4, 7.0, 5.4)
S.arrow(ax, 8.4, 4.6, 1.7, 2.6); S.arrow(ax, 3.2, 1.8, 3.7, 1.8); S.arrow(ax, 6.5, 1.8, 7.0, 1.8)
S.label(ax, 4.6, 2.85, "denied fact: swap in the priced alternative", fs=9.5)
save(fig, 4, kind="diagram")
