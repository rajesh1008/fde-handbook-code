"""Figure 35.4: Caldwell's decision path and where the state-law questions attach."""
from _common import S, save, blank
fig, ax = S.figure(height=4.6); blank(ax, (0, 10), (0, 8))
steps = [("claim file", "data"), ("summary draft", "model"), ("adjuster decides", "approval"), ("payment", "system")]
for i, (t, r) in enumerate(steps):
    S.box(ax, 0.15 + i * 2.5, 5.2, 2.2, 1.5, t, role=r, fs=10)
    if i:
        S.arrow(ax, i * 2.5 - 0.15, 5.95, i * 2.5 + 0.15, 5.95)
S.box(ax, 2.65, 1.2, 2.2, 2.1, "medical bills:\nsensitive data", role="blocker", fs=9.5)
S.box(ax, 5.15, 1.2, 2.2, 2.1, "significant\ndecision?\ncounsel", role="blocker", fs=9.5)
S.box(ax, 7.65, 1.2, 2.2, 2.1, "C06-ft1\nweights:\nretention?", role="cost", fs=9.5)
S.arrow(ax, 1.25, 5.2, 3.7, 3.3); S.arrow(ax, 6.25, 5.2, 6.25, 3.3); S.arrow(ax, 3.75, 5.2, 8.7, 3.3)
save(fig, 4, kind="diagram", data="04-code/ch35/output/regimes.txt")
