"""Figure 5.5: where a reusable field fix goes in each home, and what closes it."""
from _common import S, save, blank, plt, HOME_ROLE
from homes import HOMES

fig, ax = plt.subplots(figsize=(S.WIDTH_IN, 4.0)); blank(ax, (0, 10), (0, 6))
S.box(ax, 0.1, 2.4, 1.8, 1.2, "field fix", role="data", lw=2.8)
rows = [("vendor", "product backlog", "released;\nsecond customer"),
        ("integrator", "method library", "reused on second\nengagement"),
        ("lab", "eval case", "accepted by\nmodel team")]
assert HOMES["vendor"].reuse_route == "product backlog"
for i, (k, dest, closes) in enumerate(rows):
    y = 4.4 - i * 1.9
    S.box(ax, 3.0, y, 2.8, 1.1, dest, role=HOME_ROLE[k])
    S.box(ax, 6.9, y, 2.9, 1.1, closes, role="approval")
    S.arrow(ax, 1.9, 3.0, 3.0, y + 0.55)
    S.arrow(ax, 5.8, y + 0.55, 6.9, y + 0.55)
S.label(ax, 4.4, 5.75, "route", fs=10, ha="center")
S.label(ax, 8.35, 5.75, "closes when", fs=10, ha="center")
save(fig, 5, kind="diagram")
