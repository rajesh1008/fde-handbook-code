"""Figure 33.6: documents whose 20 runs varied, by field; variation flags only some errors."""
import re
from _common import S, save, text
t = text("evidence")
rows = re.findall(r"^  ([a-z_]+) +([\d.]+)% +([\d.]+)% +([\d.]+) +([\d.]+)%  (\d+) of (\d+)$", t, re.M)
rows = sorted(rows, key=lambda r: float(r[4]))
fig, ax = S.figure(height=4.6)
for i, r in enumerate(rows):
    judg = r[0] in ("claimant_name", "loss_location", "other_party")
    role = "data" if judg else "evidence"
    ax.barh(i, float(r[4]), color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white", height=0.6)
    ax.text(float(r[4]) + 0.3, i, f"{r[4]}%  ({r[5]} of {r[6]} errors)", va="center", fontsize=9)
ax.set_yticks(range(len(rows)), [r[0] for r in rows], fontsize=9, family="monospace")
ax.set_xlim(0, 30); ax.set_xlabel("documents whose 20 runs did not all agree (%)")
ax.text(29.5, 0, "amber: judgment fields", ha="right", va="center", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 6, data="04-code/ch33/output/evidence.txt")
