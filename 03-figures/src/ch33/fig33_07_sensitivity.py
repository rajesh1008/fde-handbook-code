"""Figure 33.7: accuracy lost under three conditions; three pairs cross the 10-point limit line."""
import re
from _common import S, save, text
t = text("evidence")
sec = t.split("SENSITIVITY")[1].split("LIMITS")[0]
rows = re.findall(r"^  ([a-z_]+) +([\d.]+)% +([\d.]+)% +([\d.]+)% +([\d.]+)%$", sec, re.M)
conds = [("fax noise", "evidence", "o"), ("rotated page", "blocker", "s"), ("handwritten", "cost", "^")]
fig, ax = S.figure(height=4.6)
for i, r in enumerate(rows):
    clean = float(r[1])
    for j, (c, role, mk) in enumerate(conds):
        d = clean - float(r[2 + j])
        ax.plot(d, i, marker=mk, color=S.ROLE[role], markersize=7, linestyle="none", label=c if i == 0 else None)
ax.axvline(10, color=S.PAL["coral"], lw=S.LW["control"], ls="--")
ax.text(10.4, len(rows) - 0.6, "limit: 10 points", fontsize=9, color=S.PAL["ink"])
ax.set_yticks(range(len(rows)), [r[0] for r in rows], fontsize=9, family="monospace"); ax.invert_yaxis()
ax.set_xlabel("accuracy lost against clean pages (points)"); ax.set_xlim(-5, 25)
ax.legend(loc="lower right", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 7, data="04-code/ch33/output/evidence.txt")
