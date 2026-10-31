"""Figure 8.5: chance agreement between two scorers rises with the share of fields that are right."""
from _common import S, plt, save
import numpy as np
p = np.linspace(0.5, 0.99, 200)
fig, ax = S.figure(3.7)
ax.plot(p * 100, (p * p + (1 - p) * (1 - p)) * 100, color=S.ROLE["model"], lw=1.5)
for q in (0.90, 0.95):
    c = q * q + (1 - q) ** 2
    ax.plot([q * 100], [c * 100], "o", color=S.ROLE["blocker"])
    ax.text(q * 100 - 1, c * 100 + 2.5, f"{q:.0%} right: {c:.0%} by chance", fontsize=9, ha="right")
ax.set_xlabel("share of fields the system got right (%)"); ax.set_ylabel("agreement expected by chance (%)")
ax.set_ylim(45, 100)
save(fig, 5, data="formula p^2 + (1-p)^2, two independent scorers with equal pass rates")
