"""Figure 33.4: what Caldwell's data changes, and what it does not."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4); blank(ax, (0, 10), (0, 7))
S.box(ax, 3.3, 2.9, 3.4, 1.3, "provider model\nweights unchanged", role="model", lw=S.LW["emphasis"])
for x, y, t in [(0.2, 5.3, "prompt"), (3.6, 5.3, "retrieval index"), (7.0, 5.3, "thresholds"),
                (0.2, 2.9, "examples")]:
    S.box(ax, x, y, 2.8, 1.0, t, role="evidence")
S.label(ax, 5.0, 6.55, "design choices: reviewed as part of the use", ha="center", fs=9.5)
S.box(ax, 0.2, 0.3, 4.2, 1.2, "router map\nfitted on cal-600", role="data", lw=S.LW["emphasis"])
S.box(ax, 5.6, 0.3, 4.2, 1.2, "C06-ft1 weights\ntrained on history-6000", role="data", lw=S.LW["emphasis"])
S.label(ax, 5.0, 1.85, "changed by Caldwell data: full scope", ha="center", fs=9.5)
for x in (1.6, 5.0, 8.4):
    S.arrow(ax, x, 5.3, 5.0 if x != 5.0 else 5.0, 4.2, weight="data")
S.arrow(ax, 3.0, 3.4, 3.3, 3.4, weight="data")
save(fig, 4, kind="diagram", data="04-code/ch33/world.py")
