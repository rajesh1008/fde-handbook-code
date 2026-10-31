"""Figure 1.4: do you need forward deployed engineers at all? Deployment complexity against what the buyer buys."""
from _common import S, save, tbox
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8.5, 6)); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
q = [(0.3, 0.3, "self-serve and documentation\nthe product configures in a day;\nthe buyer wants a tool", "evidence"),
     (5.2, 0.3, "solutions engineers and\nprofessional services\nhard to install; the buyer\nruns it once it works", "system"),
     (0.3, 5.2, "customer success and\nconfiguration services\nsimple product; the buyer\nwants a business result", "data"),
     (5.2, 5.2, "forward deployed engineers\nmany systems, controls, unstated rules;\nthe buyer pays for an outcome\nit cannot build itself", "approval")]
for x, y, t, role in q:
    tbox(ax, x, y, 4.5, 4.2, t, role=role, fs=9, fill_alpha=0.12)
for name, x, y in [("Caldwell", 8.6, 5.9), ("Greystone", 7.2, 6.25), ("Pennant", 5.8, 5.7)]:
    ax.plot(x, y, "o", color=S.PAL["ink"], ms=6); ax.text(x + 0.15, y + 0.15, name, fontsize=8.5)
ax.annotate("", xy=(9.9, -0.35), xytext=(0.1, -0.35), arrowprops=dict(arrowstyle="-|>", color=S.PAL["ink"]), annotation_clip=False)
ax.text(5, -0.8, "deployment complexity: systems, data, controls to cross", ha="center", fontsize=9)
ax.annotate("", xy=(-0.35, 9.9), xytext=(-0.35, 0.1), arrowprops=dict(arrowstyle="-|>", color=S.PAL["ink"]), annotation_clip=False)
ax.text(-0.8, 5, "what the buyer buys: a tool → an outcome", rotation=90, va="center", ha="center", fontsize=9)
save(fig, 4)
