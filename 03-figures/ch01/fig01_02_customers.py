"""Figure 1.2: the three customers this book follows, and the fourth that arrives in Part VIII (fieldkit fixtures)."""
from _common import S, save, tbox
import matplotlib.pyplot as plt
from fieldkit.fixtures import CUSTOMERS
work = {"caldwell": "claims intake: documents\nto structured claims",
        "greystone": "clinical notes summarised\nfor clinicians",
        "pennant": "paper and EDI freight\ndocuments to bookings",
        "harbourline": "a shadow build under\na regulator's eye"}
gate = {"caldwell": "Priya Natarajan,\nenterprise architect", "greystone": "Sam Oakley,\nSecurity Lead",
        "pennant": "Jenna Ruiz,\nVP Operations", "harbourline": "Helen Marsh,\nHead of Model Risk"}
fig, ax = plt.subplots(figsize=(10, 4.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 4.6); ax.axis("off")
for i, k in enumerate(["caldwell", "greystone", "pennant", "harbourline"]):
    c = CUSTOMERS[k]; x = 0.1 + i * 2.5
    role = "system" if k != "harbourline" else "evidence"
    tbox(ax, x, 0.35, 2.3, 3.9, "", role=role, fill_alpha=0.10 if k != "harbourline" else 0.04)
    bb = dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.94)
    ax.text(x + 1.15, 3.85, c["name"], ha="center", fontsize=10, weight="bold", color=S.PAL["ink"], bbox=bb)
    ax.text(x + 1.15, 3.4, f"{c['city']} · {c['cloud']}\n{c['contract']}", ha="center", va="top", fontsize=8.5, bbox=bb)
    ax.text(x + 1.15, 2.5, work[k], ha="center", va="top", fontsize=8.3, bbox=bb)
    ax.text(x + 1.15, 1.45, "first hard question from\n" + gate[k], ha="center", va="top", fontsize=8, style="italic", bbox=bb)
    if k == "harbourline":
        ax.text(x + 1.15, 0.55, "fourth customer: Part VIII", ha="center", fontsize=8, color=S.PAL["slate"], bbox=bb)
save(fig, 2)
