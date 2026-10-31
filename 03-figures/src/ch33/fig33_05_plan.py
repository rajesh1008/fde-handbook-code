"""Figure 33.5: the 71 plan items by outcome; full scope is two components and 20 items."""
import re
from _common import S, save, text
t = text("pack_v1")
rows = re.findall(r"^  (.+?) +(\d+) items each: (.*)$", t, re.M)
role = {"not a model": "system", "registered, not validated": "evidence", "registered as a tool": "data",
        "full scope": "approval"}
fig, ax = S.figure(height=3.8)
data = [(o, int(k), len(ids.split(", "))) for o, k, ids in rows]
for i, (o, k, n) in enumerate(data):
    ax.barh(i, k * n, color=S.ROLE[role[o]], hatch=S.HATCH[role[o]], edgecolor="white", height=0.6)
    ax.text(k * n + 0.6, i, f"{k * n} items ({n} x {k})", va="center", fontsize=10)
ax.set_yticks(range(len(data)), [o for o, *_ in data]); ax.invert_yaxis()
ax.set_xlim(0, 50); ax.set_xlabel("validation plan items"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch33/output/pack_v1.txt")
