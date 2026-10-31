"""Figure 24.1: where adjusters and intake clerks spend their logged minutes (day 104 sample, options.txt)."""
import re
from _common import S, save, text
rows = re.findall(r"^  (adjusters|intake clerks)\s+suite \d+%: (.+)$", text("options"), re.M)
col = {"suite mail and calendar": S.PAL["navy"], "suite chat and meetings": S.PAL["slate"], "suite documents": S.PAL["teal"],
       "claims-core": S.PAL["amber"], "intake queue tool": S.PAL["plum"], "phone and other": S.PAL["grey"]}
short = {"suite mail and calendar": "mail", "suite chat and meetings": "chat", "suite documents": "docs",
         "claims-core": "claims-core", "intake queue tool": "queue tool", "phone and other": "other"}
fig, ax = S.figure(height=4.0)
for i, (g, parts) in enumerate(rows):
    left = 0; y = 1 - i
    for k, v in re.findall(r"([a-z -]+?) (\d+)%", parts):
        k = k.strip(); v = int(v)
        ax.barh(y, v, left=left, color=col[k], height=0.5, edgecolor="white")
        if v >= 6:
            ax.text(left + v / 2, y, f"{short[k]}\n{v}%", ha="center", va="center", fontsize=10, color=S.text_on(col[k]),
                    bbox=dict(boxstyle="square,pad=0.1", fc=col[k], ec="none"))
        left += v
    suite = sum(int(v) for k, v in re.findall(r"(suite [a-z ]+?) (\d+)%", parts))
    ax.text(0, y + 0.36, f"in the suite: {suite}%", fontsize=10, color=S.PAL["ink"], weight="bold")
ax.set_yticks([1, 0], [r[0] for r in rows]); ax.set_ylim(-0.6, 1.6); ax.set_xlim(0, 100)
ax.set_xlabel("share of logged working minutes, 5 days (stand-in)")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 1, data="04-code/ch24/output/options.txt")
