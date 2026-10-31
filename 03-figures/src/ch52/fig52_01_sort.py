"""Figure 52.1: the sort. What changes by 2029 sits on the left; what does not sits on the right."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4)
blank(ax, (0, 10), (0, 6.2))
S.label(ax, 2.4, 5.8, "Changes by 2029", fs=12, fontweight="bold")
S.label(ax, 7.6, 5.8, "Does not change", fs=12, fontweight="bold")
left = ["Price per document", "Model behind the pin", "Connectors and tooling", "Who runs the suite"]
right = ["The expert's gold set", "A named person signs", "Deterministic first", "Evidence a stranger rebuilds"]
for i, (a, b) in enumerate(zip(left, right)):
    y = 4.55 - i * 1.25
    S.box(ax, 0.3, y, 4.2, 0.9, a, role="cost", fs=10.5)
    S.box(ax, 5.5, y, 4.2, 0.9, b, role="approval", fs=10.5, lw=S.LW["emphasis"])
S.label(ax, 5.0, 0.1, "Every new model is checked against the right column", fs=10, ha="center")
save(fig, 1, kind="diagram", data="Chapter 52 argument, Sections 52.1 and 52.2")
