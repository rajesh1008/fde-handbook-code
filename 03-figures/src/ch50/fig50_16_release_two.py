"""Figure 50.16: the approval path for release two (writes); four signatures, none given as of day 171."""
from _common import S, save, text, blank
assert "none given as of day 171" in text("boundary")
steps = [("Marsh: reclassify\nwith writes", "evidence"), ("Shaw: write path\narchitecture", "system"),
         ("Okafor: op risk,\nSchedule D", "approval"), ("Dubois: contract\namendment", "evidence")]
fig, ax = S.figure(height=3.8); blank(ax, (0, 10), (0, 6))
for i, (t, r) in enumerate(steps):
    x = 0.1 + i * 2.5
    S.box(ax, x, 3.6, 2.2, 1.3, t, role=r, fs=9.5, ls="--")
    if i < 3:
        S.arrow(ax, x + 2.2, 4.25, x + 2.5, 4.25, weight="data")
S.arrow(ax, 5.0, 3.55, 5.0, 2.55)
S.box(ax, 2.0, 1.2, 6.0, 1.3, "write to origination, uat first,\neach write approved by the officer", role="data", fs=9.5)
S.label(ax, 5.0, 0.45, "dashed: not signed as of day 171", fs=9.5, ha="center")
save(fig, 16, kind="diagram", data="04-code/ch50/output/boundary.txt")
