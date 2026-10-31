"""Figure 17.7: Harbourline's outbound proxy re-signs TLS; the runner must trust the bank's authority, not pin the provider."""
from _common import S, save, blank
fig, ax = S.figure(height=3.8)
blank(ax, (0, 10), (0, 6))
S.box(ax, 0.1, 3.4, 2.2, 1.3, "runner", role="system", lw=S.LW["emphasis"])
S.box(ax, 3.4, 3.4, 3.0, 1.3, "bank proxy\nre-signs TLS", role="blocker")
S.box(ax, 7.5, 3.4, 2.4, 1.3, "model\nendpoint", role="model")
S.box(ax, 0.1, 0.5, 2.2, 1.4, "bank CA\nbundle", role="data")
S.box(ax, 3.4, 0.5, 3.0, 1.4, "pinned provider\ncertificate: fails", role="blocker", ls="--")
S.arrow(ax, 2.3, 4.05, 3.4, 4.05); S.arrow(ax, 6.4, 4.05, 7.5, 4.05); S.arrow(ax, 1.2, 1.9, 1.2, 3.4, weight="data")
S.label(ax, 0.1, 5.4, "trust what the bank's network presents", fs=10, color=S.PAL["slate"])
save(fig, 7, kind="diagram", data="chapter text (Harbourline)")
