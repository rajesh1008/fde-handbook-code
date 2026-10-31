"""Figure 21.2: weight mismatches on 600 freight legs, raw field against raw field versus like against like."""
import re
from _common import S, save, text
t = text("register")
raw = float(re.search(r"raw field: \d+ \(([\d.]+)%", t).group(1))
reg = float(re.search(r"chargeable against chargeable: \d+ \(([\d.]+)%", t).group(1))
fig, ax = S.figure(height=3.7)
bars = ax.barh([1, 0], [raw, reg], color=[S.ROLE["blocker"], S.ROLE["approval"]], height=0.55)
ax.set_yticks([1, 0], ["TMS gross kg vs\ncarrier billed weight", "chargeable vs\nchargeable"])
for y, v in ((1, raw), (0, reg)):
    ax.text(v + 1, y, f"{v:.1f}%", va="center", fontsize=11, color=S.PAL["ink"])
ax.set_xlim(0, 60); ax.set_xlabel("legs flagged as weight mismatch (%)")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 2, data="04-code/ch21/output/register.txt")
