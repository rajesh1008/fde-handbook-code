"""Figure 33.1: one system, two one-model answers, and the component test."""
from _common import S, save, blank
fig, ax = S.figure(height=4.2); blank(ax, (0, 10), (0, 7))
S.box(ax, 0.2, 5.3, 4.4, 1.3, "Caldwell, day 74:\none model, tier 1", role="blocker")
S.box(ax, 5.4, 5.3, 4.4, 1.3, "Northlight, day 76:\noutside scope", role="blocker")
S.label(ax, 2.4, 4.75, "6 of 14 items unanswerable", ha="center", fs=9.5)
S.label(ax, 7.6, 4.75, "4 core uses untested", ha="center", fs=9.5)
S.arrow(ax, 2.4, 4.5, 4.2, 3.55); S.arrow(ax, 7.6, 4.5, 5.8, 3.55)
S.box(ax, 2.0, 2.5, 6.0, 1.05, "component test, day 153: 17 components", role="system", lw=S.LW["emphasis"])
for i, (lab, r) in enumerate([("full scope\n2", "approval"), ("registered,\nnot validated 4", "evidence"),
                              ("tool\n2", "data"), ("not a model\n9", "system")]):
    S.box(ax, 0.2 + i * 2.45, 0.3, 2.2, 1.3, lab, role=r, fs=9.5)
    S.arrow(ax, 5.0, 2.5, 1.3 + i * 2.45, 1.6, weight="data")
save(fig, 1, kind="diagram", data="04-code/ch33/output/classify.txt")
