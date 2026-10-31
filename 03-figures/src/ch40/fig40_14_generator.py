"""Figure 40.14: the pack generator: resolve each element, verify it, render the pack, extend the chain."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4); blank(ax, (0, 10), (0, 8))
for i, t in enumerate(("run record", "registry", "claims-core")):
    S.box(ax, 0.1 + i * 3.4, 6.0, 2.8, 1.4, t, role="data", fs=10)
    S.arrow(ax, 1.5 + i * 3.4, 6.0, 5.0, 4.9)
S.box(ax, 0.1, 3.3, 2.8, 1.6, "resolve", role="system", fs=10)
S.box(ax, 3.5, 3.3, 2.8, 1.6, "verify", role="system", fs=10)
S.box(ax, 6.9, 3.3, 2.8, 1.6, "render", role="system", fs=10)
S.arrow(ax, 2.9, 4.1, 3.5, 4.1); S.arrow(ax, 6.3, 4.1, 6.9, 4.1)
S.box(ax, 3.5, 0.5, 2.8, 1.6, "pack, digest", role="approval", fs=10)
S.box(ax, 6.9, 0.5, 2.8, 1.6, "chain head", role="evidence", fs=10)
S.arrow(ax, 8.3, 3.3, 4.9, 2.1); S.arrow(ax, 6.3, 1.3, 6.9, 1.3)
save(fig, 14, kind="diagram", data="04-code/ch40/pack.py (build, render, chain_head)")
