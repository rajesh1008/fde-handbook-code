"""Figure 47.1: what repeats across twenty engagements: engagements that built each component, colored by the shape rule."""
from _common import S, save, text
rows = []
for l in text("repeats").splitlines()[1:]:
    if not l.strip() or l.startswith(("bespoke", "rule")):
        continue
    comp = l[:38].strip(); f = l[38:].split()
    rows.append((comp, int(f[0]), int(f[1]), f[4]))
rows = rows[::-1]
col = dict(platform=("system", "//"), playbook=("data", ".."), bespoke=("blocker", "\\\\"))
fig, ax = S.figure(height=5.6)
for i, (c, n, v, k) in enumerate(rows):
    ax.barh(i, n, 0.7, color=S.ROLE[col[k][0]], hatch=col[k][1], ec="white")
    ax.text(n + 0.3, i, f"{v} shape" + ("s" if v > 1 else ""), va="center", fontsize=9)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=9)
ax.axvline(8, color=S.PAL["ink"], ls="--", lw=0.75); ax.text(8.2, len(rows) - 0.4, "8 engagements", fontsize=9)
ax.set_xlim(0, 25); ax.set_xlabel("engagements that built it (of 20)")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc=S.ROLE[col[k][0]], hatch=col[k][1], ec="white", label=k) for k in col],
          loc="lower right", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 1, data="04-code/ch47/output/repeats.txt")
