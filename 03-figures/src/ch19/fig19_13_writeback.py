"""Figure 19.12: the write-back path: outbox, preflight, screens, read-back; every exit is a state."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4)
blank(ax, (0, 12), (0, 7.2))
main = [("outbox\n+ key", "data"), ("preflight\nrules", "evidence"), ("screens\n1 and 2", "system"),
        ("read back", "evidence"), ("verified", "approval")]
for i, (t, r) in enumerate(main):
    x = 0.1 + i * 2.4
    S.box(ax, x, 4.4, 1.9, 1.5, t, role=r, fs=10)
    if i < 4:
        S.arrow(ax, x + 1.9, 5.15, x + 2.4, 5.15)
S.box(ax, 2.5, 1.0, 7.1, 1.3, "held: a person owns it", role="blocker", fs=10.5)
for x in (3.45, 5.85, 8.25):
    S.arrow(ax, x, 4.4, x if x != 5.85 else 6.0, 2.3, ls="--", weight="data")
S.label(ax, 6.1, 3.2, "void shell", fs=9.5)
S.label(ax, 5.0, 6.5, "timeout: find by key, then verify", fs=9.5, color=S.PAL["slate"])
save(fig, 13, kind="diagram", data="fieldkit.connectors.WriteBack; 04-code/ch19/writeback_fixed.py")
