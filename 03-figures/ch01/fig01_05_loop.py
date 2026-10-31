"""Figure 1.5: the six verbs of the job as a loop around the evidence the engagement leaves."""
import math
from _common import S, save, tbox
import matplotlib.pyplot as plt
verbs = [("discover", "data", "find the real workflow\nand the unstated rules"),
         ("decide", "evidence", "what needs a model,\nwhat does not; log it"),
         ("access", "blocker", "earn each rung:\nsynthetic to live"),
         ("build", "system", "inside their estate,\nunder their controls"),
         ("pass", "approval", "the five gates and\nthe customer's experts"),
         ("hand over", "model", "something they can run,\ninspect and switch off")]
fig, ax = plt.subplots(figsize=(8.5, 6.2)); ax.set_xlim(-5, 5); ax.set_ylim(-3.9, 3.9); ax.axis("off")
pts = []
for i, (v, role, sub) in enumerate(verbs):
    a = math.pi / 2 - i * 2 * math.pi / 6
    x, y = 3.3 * math.cos(a), 2.8 * math.sin(a); pts.append((x, y))
    tbox(ax, x - 1.15, y - 0.55, 2.3, 1.1, f"{i + 1}. {v}\n{sub}", role=role, fs=8.5)
for i in range(6):
    x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % 6]
    ax.annotate("", xy=(x1 + 0.72 * (x2 - x1), y1 + 0.72 * (y2 - y1)), xytext=(x1 + 0.28 * (x2 - x1), y1 + 0.28 * (y2 - y1)),
                arrowprops=dict(arrowstyle="-|>", color=S.PAL["ink"], lw=1.3))
tbox(ax, -1.45, -0.6, 2.9, 1.2, "evidence\ndecision log, access tracker,\nevaluation results, runbook", role="evidence", fs=8.5, fill_alpha=0.06)
ax.text(0, -3.75, "The loop repeats at every rung; discovery does not stop when the build starts.", ha="center", fontsize=9, style="italic", color=S.PAL["ink"])
save(fig, 5)
