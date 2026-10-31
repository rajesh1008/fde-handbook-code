"""Figure 5.9: a vendor-plus-integrator split at Greystone; who owns each seam."""
from _common import S, save, blank, plt

fig, ax = plt.subplots(figsize=(S.WIDTH_IN, 4.2)); blank(ax, (0, 9), (0, 6.2))
cols = [("Northlight FDE", "evidence", ["data mapping", "evaluation", "product fixes"]),
        ("managed-service provider", "system", ["identity", "change calendar", "run support"]),
        ("Greystone", "approval", ["security sign-off", "acceptance", "cost owner"])]
for i, (who, role, seams) in enumerate(cols):
    x = 0.2 + i * 3.0
    S.box(ax, x, 5.0, 2.6, 0.9, who, role=role, lw=2.8, fs=10.5)
    for j, s in enumerate(seams):
        y = 3.7 - j * 1.35
        S.box(ax, x, y, 2.6, 0.95, s, role=role)
save(fig, 7, kind="diagram")
