"""Figure 19.11: overlay, do not replace: the core is untouched; the overlay uses doors that already exist."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4)
blank(ax, (0, 12), (0, 7.2))
S.box(ax, 0.3, 0.5, 4.2, 6.2, "", role="system", fs=10)
S.label(ax, 2.4, 6.2, "core system", fs=10.5, ha="center")
for i, t in enumerate(["screens", "export", "rule table"]):
    S.box(ax, 0.9, 4.4 - i * 1.6, 3.0, 1.0, t, role="evidence", fs=10)
S.box(ax, 6.8, 2.3, 4.8, 2.6, "overlay\n(our code, our risk)", role="model", fs=10.5)
S.arrow(ax, 6.8, 4.3, 3.9, 4.9); S.arrow(ax, 3.9, 3.3, 6.8, 3.6, ls="--", weight="data")
S.arrow(ax, 3.9, 1.7, 6.8, 2.6, ls="--", weight="data")
S.label(ax, 6.8, 1.4, "removable in a day", fs=10, color=S.PAL["slate"])
save(fig, 11, kind="diagram", data="Section 19.6")
