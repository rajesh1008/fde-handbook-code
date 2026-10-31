"""Figure 20.7: what to do when the pinned version is not offered where the data may go."""
from _common import S, save, blank
fig, ax = S.figure(height=4.2)
blank(ax, (0, 10), (0, 6))
S.box(ax, 2.6, 4.6, 4.8, 1.0, "pinned version offered\nin an allowed region?", role="evidence", fs=10)
S.box(ax, 7.9, 4.6, 1.9, 1.0, "deploy", role="approval", fs=10)
S.arrow(ax, 7.4, 5.1, 7.9, 5.1); S.label(ax, 7.5, 5.7, "yes", fs=10)
opts = [("wait", "provider date", "evidence"), ("move region", "residency owner,\nin writing", "blocker"),
        ("change the pin", "validate in region,\nrecord the change", "approval")]
for i, (o, who, role) in enumerate(opts):
    x = 0.3 + i * 3.25
    S.box(ax, x, 2.3, 2.9, 1.0, o, role=role, fs=10, lw=S.LW["emphasis"] if i == 2 else None)
    S.label(ax, x + 1.45, 1.7, who, fs=10, ha="center", va="top")
    S.arrow(ax, 5.0, 4.6, x + 1.45, 3.3)
S.label(ax, 5.15, 3.95, "no", fs=10)
S.label(ax, 0.3, 0.3, "the customer chooses; the adapter never substitutes", fs=10, color=S.PAL["slate"])
save(fig, 7, kind="diagram", data="fieldkit/estates.py UNAVAILABLE_OPTIONS")
