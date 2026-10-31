"""Figure 20.2: the private path to the model on each estate, and the public path the workload must not reach."""
from _common import S, save, blank
fig, ax = S.figure(height=4.0)
blank(ax, (0, 10), (0, 6))
lanes = [("Caldwell", "interface endpoint"), ("Greystone", "private endpoint"), ("Pennant", "service connect,\nperimeter")]
for i, (who, path) in enumerate(lanes):
    y = 4.3 - i * 1.6
    S.box(ax, 0.1, y, 1.9, 0.9, f"{who}\nrunner", role="system", fs=10)
    S.box(ax, 2.6, y, 2.6, 0.9, path, role="approval", fs=10)
    S.box(ax, 5.8, y, 1.5, 0.9, "model", role="model", fs=10)
    S.box(ax, 8.1, y, 1.8, 0.9, "public\nendpoint", role="blocker", fs=10, ls="--")
    S.arrow(ax, 2.0, y + 0.45, 2.6, y + 0.45); S.arrow(ax, 5.2, y + 0.45, 5.8, y + 0.45)
    S.label(ax, 9.0, y + 1.15, "blocked", fs=10, ha="center", va="center")
S.label(ax, 0.1, 0.2, "checks N1 to N3 prove both directions", fs=10, color=S.PAL["slate"])
save(fig, 2, kind="diagram", data="04-code/ch20/sim_clouds.py Network and output/parity.txt")
