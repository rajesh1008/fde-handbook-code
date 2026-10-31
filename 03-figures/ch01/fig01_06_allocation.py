"""Figure 1.6: time allocation, the Caldwell week versus the injected productive-looking week (lab output)."""
from _common import S, R, vstyle, save
import matplotlib.pyplot as plt
import numpy as np
import weeklog as W
a = W.load(R / "04-code/ch01/data", "week_a_caldwell", "caldwellmutual.com")
b = W.load(R / "04-code/ch01/data", "week_b_injected", "caldwellmutual.com")
fig, axes = plt.subplots(1, 2, figsize=(10, 4.8), gridspec_kw=dict(width_ratios=[2.2, 1]))
ax = axes[0]
for j, (w, lab) in enumerate([(a, "Week A: days 81-85\n(Caldwell, as lived)"), (b, "Week B: days 88-92\n(injected)")]):
    left = 0
    for v in W.BUCKETS:
        h = w.hours[v]
        if h == 0: continue
        st = vstyle(v)
        ax.barh(1 - j, h, left=left, color=st["color"], hatch=st["hatch"], edgecolor="white", height=0.55)
        if h >= 3: ax.text(left + h / 2, 1 - j, f"{h:g} h", ha="center", va="center", fontsize=8,
                           bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))
        left += h
    ax.text(left + 0.4, 1 - j, f"{sum(w.contact.values()):g} h with customer", va="center", fontsize=8.5)
ax.set_yticks([1, 0]); ax.set_yticklabels(["Week A: days 81-85\n(Caldwell, as lived)", "Week B: days 88-92\n(injected)"], fontsize=9)
ax.set_xlim(0, 46); ax.set_xlabel("calendar hours")
ax.set_title("Where the hours went", loc="left", fontsize=11)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=vstyle(v)["color"], hatch=vstyle(v)["hatch"], edgecolor="white", label=v) for v in W.BUCKETS],
          loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=4, frameon=False, fontsize=8)
ax2 = axes[1]
labels = ["commits", "tickets\nclosed", "customer items\nmoved"]
va = [sum(a.commits.values()), a.tickets_closed, len(a.customer_items_moved)]
vb = [sum(b.commits.values()), b.tickets_closed, len(b.customer_items_moved)]
x = np.arange(3)
ax2.bar(x - 0.2, va, 0.4, color=S.ROLE["system"], hatch="//", edgecolor="white", label="Week A")
ax2.bar(x + 0.2, vb, 0.4, color=S.ROLE["blocker"], hatch="\\\\", edgecolor="white", label="Week B")
for i in range(3):
    ax2.text(i - 0.2, va[i] + 0.8, str(va[i]), ha="center", fontsize=8.5)
    ax2.text(i + 0.2, vb[i] + 0.8, str(vb[i]), ha="center", fontsize=8.5)
ax2.set_xticks(x); ax2.set_xticklabels(labels, fontsize=8); ax2.legend(frameon=False, fontsize=8)
ax2.set_title("What a dashboard sees", loc="left", fontsize=11)
fig.tight_layout()
save(fig, 6)
