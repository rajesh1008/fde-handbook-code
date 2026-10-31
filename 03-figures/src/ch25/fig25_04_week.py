"""Figure 25.4: calls the planner emitted in the shadow week, by authorizer result."""
import re
from _common import S, save, text
t = text("authorize_week")
rows = re.findall(r"^\s+(\w+)\s+(\S+)\s+(\d+)$", t, re.M)
fig, ax = S.figure(height=3.7)
labels = [f"{op}\n{res.replace('denied:', 'denied, ')}" for op, res, _ in rows]
vals = [int(n) for *_, n in rows]
colors = [S.ROLE["approval"] if "allowed" in r else S.ROLE["blocker"] for _, r, _ in rows]
y = range(len(rows))[::-1]
ax.barh(list(y), vals, color=colors, height=0.6)
ax.set_xscale("log"); ax.set_xlim(0.8, 3000)
for yy, v in zip(y, vals):
    ax.text(v * 1.15, yy, f"{v:,}", va="center", fontsize=10, color=S.PAL["ink"])
ax.set_yticks(list(y), labels, fontsize=9.5)
ax.set_xlabel("calls (log scale)")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 4, data="04-code/ch25/output/authorize_week.txt")
