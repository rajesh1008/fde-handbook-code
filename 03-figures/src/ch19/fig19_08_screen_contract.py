"""Figure 19.8: a screen treated as a contract: recognize, act, then prove it."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 12), (0, 6))
steps = [("fingerprint\nthe labels", "evidence"), ("fill by\nlabel", "system"), ("submit", "system"),
         ("read back\nevery field", "evidence")]
for i, (t, r) in enumerate(steps):
    x = 0.2 + i * 3.0
    S.box(ax, x, 3.3, 2.4, 1.5, t, role=r, fs=10)
    if i < 3:
        S.arrow(ax, x + 2.4, 4.05, x + 3.0, 4.05)
S.box(ax, 0.2, 0.7, 2.4, 1.2, "stop, alarm", role="blocker", fs=10)
S.arrow(ax, 1.4, 3.3, 1.4, 1.9, ls="--", weight="data")
S.box(ax, 9.2, 0.7, 2.4, 1.2, "hold", role="blocker", fs=10)
S.arrow(ax, 10.4, 3.3, 10.4, 1.9, ls="--", weight="data")
S.label(ax, 3.4, 1.2, "changed screen or wrong value", fs=10, color=S.PAL["slate"])
save(fig, 8, kind="diagram", data="fieldkit.connectors.ScreenConnector")
