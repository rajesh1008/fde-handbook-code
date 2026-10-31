"""Figure 5.1: three homes, three fixed points; what bends and how each ends."""
from _common import S, save, blank, plt, HOME_ROLE
from homes import HOMES

fig, ax = plt.subplots(figsize=(S.WIDTH_IN, 4.0)); blank(ax, (0, 9), (0, 6))
cols = [("vendor", "product vendor", "fixed: the product", "bends: the workflow", "ends: product support"),
        ("integrator", "integrator", "fixed: the platform", "bends: the method", "ends: contract end"),
        ("lab", "model lab", "fixed: the model", "bends: the deployment", "ends: partner hand-over")]
assert [HOMES[k].fixed.split()[-1] for k, *_ in cols] == ["product", "platform", "model"]
for i, (k, name, fixed, bends, ends) in enumerate(cols):
    x = 0.2 + i * 3.0
    S.label(ax, x + 1.3, 5.6, name, fs=11, ha="center", weight="bold")
    S.box(ax, x, 3.9, 2.6, 1.2, fixed, role=HOME_ROLE[k], lw=2.8)
    S.box(ax, x, 2.2, 2.6, 1.1, bends, role="data", ls="--")
    S.arrow(ax, x + 1.3, 3.9, x + 1.3, 3.3)
    S.box(ax, x, 0.5, 2.6, 1.1, ends, role="approval")
    S.arrow(ax, x + 1.3, 2.2, x + 1.3, 1.6)
save(fig, 1, kind="diagram")
