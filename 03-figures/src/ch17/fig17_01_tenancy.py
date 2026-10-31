"""Figure 17.1: four tenancy options by how many controls the customer holds, and where each customer landed."""
import re
from _common import S, save, blank, text
fig, ax = S.figure(height=4.2)
blank(ax, (-0.2, 10.2), (0, 6.4))
rows = re.findall(r"^  (\S+)\s+(.+?)\s{2,}customer holds: (.+)$", text("tenancy"), re.M)
who = {"customer-account": "Caldwell, Pennant", "customer-operated": "Greystone, Harbourline"}
for i, (key, label, holds) in enumerate(rows):
    n = 0 if holds == "nothing" else len(holds.split(", "))
    y = 0.4 + i * 1.4
    S.label(ax, 4.3, y + 0.5, label, fs=10, va="center", ha="right")
    S.box(ax, 4.5, y + 0.1, 0.25 + n * 0.3, 0.8, "", role="system", lw=S.LW["control"])
    S.label(ax, 4.85 + n * 0.3, y + 0.5, f"{n} of 6", fs=10, va="center")
    if key in who:
        S.label(ax, 7.5, y + 0.5, who[key], fs=10, va="center", weight="bold")
S.label(ax, 4.5, 6.0, "controls the customer holds", fs=10, color=S.PAL["slate"])
save(fig, 1, kind="diagram", data="04-code/ch17/output/tenancy.txt")
