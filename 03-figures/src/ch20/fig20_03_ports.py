"""Figure 20.3: one core, five ports, one thin adapter per cloud."""
from _common import S, save, blank
fig, ax = S.figure(height=4.0)
blank(ax, (0, 10), (0, 6))
S.box(ax, 2.2, 4.4, 5.6, 1.2, "core: evaluation suite, gateway adapter, connectors", role="system", fs=10, lw=S.LW["emphasis"])
for i, p in enumerate(["identity", "secrets", "model", "logs", "network"]):
    S.box(ax, 0.3 + i * 1.95, 2.8, 1.7, 0.8, p, role="evidence", fs=10)
    S.arrow(ax, 1.15 + i * 1.95, 4.4, 1.15 + i * 1.95, 3.6, weight="data")
for i, (c, role) in enumerate([("AWS adapter\n16 lines", "model"), ("Azure adapter\n11 lines", "model"), ("Google Cloud\nadapter, 10 lines", "model")]):
    S.box(ax, 0.6 + i * 3.2, 0.9, 2.6, 1.1, c, role=role, fs=10)
    S.arrow(ax, 1.9 + i * 3.2, 2.8, 1.9 + i * 3.2, 2.0, weight="data")
S.label(ax, 0.3, 0.3, "the core never imports a cloud SDK", fs=10, color=S.PAL["slate"])
save(fig, 3, kind="diagram", data="04-code/ch20/output/loc.txt and adapters.py")
