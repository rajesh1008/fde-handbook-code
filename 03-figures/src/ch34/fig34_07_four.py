"""Figure 34.7: service levels designed for all four customers: monthly sample needed and breach chance today."""
import re
from _common import S, save, text
rows = re.findall(r"^  (Caldwell|Greystone|Pennant|Harbourline) +(.+?) +[\d.]+% +[\d.]+% +(\d+) +\d+ \( ?[\d.]+%\) +"
                  r"[\d.]+% +([\d.]+)%", text("sl"), re.M)
fig, ax = S.figure(height=4.8)
roles = {"Caldwell": "model", "Greystone": "system", "Pennant": "data", "Harbourline": "evidence"}
for i, (c, m, n, p) in enumerate(rows):
    ax.barh(i, int(n), color=S.ROLE[roles[c]], hatch=S.HATCH[roles[c]], edgecolor="white", height=0.6)
    ax.text(int(n) + 8, i, f"n {n}; now {p}%", va="center", fontsize=9.5)
ax.set_yticks(range(len(rows)), [f"{c}: {m.strip()}" for c, m, _, _ in rows], fontsize=9.5)
ax.set_xlim(0, 900); ax.set_xlabel("items the customer scores each month")
ax.invert_yaxis(); ax.spines[["top", "right"]].set_visible(False)
save(fig, 7, data="04-code/ch34/output/sl.txt")
