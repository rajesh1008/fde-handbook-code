"""Figure 20.1: the identity chain on each estate, from workload to model call."""
from _common import S, save, blank
fig, ax = S.figure(height=4.0)
blank(ax, (0, 10), (0, 6))
lanes = [("Caldwell, AWS", "task role", "gateway key,\nsecret store"),
         ("Greystone, Azure", "managed identity", "token per call"),
         ("Pennant, Google Cloud", "service account", "short-lived token")]
for i, (who, ident, cred) in enumerate(lanes):
    y = 4.3 - i * 1.6
    S.label(ax, 0.1, y + 0.45, who, fs=10)
    S.box(ax, 3.0, y, 2.2, 0.9, ident, role="approval", fs=10)
    S.box(ax, 5.7, y, 2.3, 0.9, cred, role="data", fs=10)
    S.box(ax, 8.5, y, 1.4, 0.9, "model", role="model", fs=10)
    S.arrow(ax, 5.2, y + 0.45, 5.7, y + 0.45); S.arrow(ax, 8.0, y + 0.45, 8.5, y + 0.45)
S.label(ax, 3.0, 0.2, "no key files anywhere in the chain", fs=10, color=S.PAL["slate"])
save(fig, 1, kind="diagram", data="04-code/ch20/estate_configs.py and adapters.py")
