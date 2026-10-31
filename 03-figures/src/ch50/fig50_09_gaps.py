"""Figure 50.9: why the committee returned the first pack; 27 lint findings by evidence item."""
from _common import S, save, text, bar_style
rows = [l.split() for l in text("committee_s1").splitlines() if l.startswith("  missing") or l.startswith("  no monitoring")]
data = [(" ".join(r[:2]) if r[0] == "missing" else "no monitoring metric", int(r[2] if r[0] == "missing" else r[3])) for r in rows]
data = [(n.replace("missing ", "").replace("_", " "), v) for n, v in data]
fig, ax = S.figure(height=3.8)
for i, (n, v) in enumerate(data[::-1]):
    ax.barh(i, v, color=S.TINT["blocker"], edgecolor=S.ROLE["blocker"], hatch=S.HATCH["blocker"], lw=S.LW["control"])
    ax.text(v + 0.1, i, str(v), va="center", fontsize=9.5)
ax.set_yticks(range(len(data))); ax.set_yticklabels([n for n, _ in data[::-1]]); ax.set_xlim(0, 8)
ax.set_xlabel("components with the finding, submission one"); bar_style(ax)
save(fig, 9, data="04-code/ch50/output/committee_s1.txt")
