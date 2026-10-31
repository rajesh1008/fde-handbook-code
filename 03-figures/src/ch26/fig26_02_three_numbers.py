"""Figure 26.2 (sidebar): three true numbers about the same model."""
import re
from _common import S, save, text
t = text("vendor_vs_customer")
v = [float(x) for x in re.findall(r"\s([\d.]+)%(?:\s|$)", t)[:4]]
lt = float(re.search(r"loss_type\s+judge\s+[\d.]+%\s+adjusters\s+([\d.]+)%", t).group(1))
rows = [("Northlight: all ten fields,\nits own 300 cases", v[0], "model"),
        ("Caldwell: all ten fields,\nAnne's 300 documents", v[3], "evidence"),
        ("Adjusters: cause-of-loss\ncode only", lt, "blocker")]
fig, ax = S.figure(height=3.8)
for i, (lab, val, r) in enumerate(rows[::-1]):
    ax.barh(i, val, color=S.ROLE[r], hatch=S.HATCH[r], edgecolor="white", height=0.55)
    ax.text(val + 1.5, i, f"{val:.1f}%", va="center", fontsize=11, color=S.PAL["ink"])
ax.set_yticks(range(3), [r[0] for r in rows[::-1]], fontsize=9)
ax.set_xlim(0, 105); ax.set_xlabel("share scored correct (%)")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 2, data="04-code/ch26/output/vendor_vs_customer.txt")
