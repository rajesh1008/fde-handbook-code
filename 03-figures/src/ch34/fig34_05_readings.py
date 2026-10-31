"""Figure 34.5: one accuracy clause, four readings already in the engagement record."""
import re
from _common import S, save, text
rows = re.findall(r"^  (.+?) +([\d.]+)%   (met|missed)", text("readings"), re.M)
fig, ax = S.figure(height=4.6)
for i, (r, v, st) in enumerate(rows):
    role = "approval" if st == "met" else "blocker"
    ax.barh(i, float(v), color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white", height=0.6)
    ax.text(float(v) + 0.2, i, f"{v}%", va="center", fontsize=9.5)
ax.axvline(98, color=S.PAL["ink"], lw=1.5, ls="--"); ax.text(97.8, -0.45, "clause: 98%", ha="right", fontsize=9.5)
ax.set_yticks(range(len(rows)), [r.strip() for r, _, _ in rows], fontsize=9.5)
ax.set_xlim(80, 101); ax.set_xlabel("percent accurate under each reading")
ax.invert_yaxis(); ax.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch34/output/readings.txt")
