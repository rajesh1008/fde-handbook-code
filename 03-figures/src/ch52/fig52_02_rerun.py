"""Figure 52.2: two generations after the pin, weighted accuracy rises 1.9 points and cost per document falls by more than half."""
from _common import S, save, text, nums
rows = [l.split() for l in text("rerun").splitlines() if l.startswith("gm-")][:3]
names = [r[0] for r in rows]
acc = [float(r[1].rstrip("%")) for r in rows]; cost = [float(r[6]) * 1000 for r in rows]
assert names == ["gm-2026-05-14", "gm-n1", "gm-n2"] and acc[2] == 94.8
fig, (a, b) = S.figure(height=4.2, ncols=2)
roles = ["evidence", "system", "model"]
for ax, vals, ttl, fmt in ((a, acc, "Weighted accuracy, %", "{:.1f}"), (b, cost, "Model cost, $ per 1,000 documents", "{:.1f}")):
    for i, v in enumerate(vals):
        ax.bar(i, v, color=S.TINT[roles[i]], edgecolor=S.ROLE[roles[i]], hatch=S.HATCH[roles[i]], lw=S.LW["control"])
        ax.text(i, v + (0.15 if ax is a else 0.2), fmt.format(v), ha="center", fontsize=10)
    ax.set_xticks(range(3)); ax.set_xticklabels(["pin", "n+1", "n+2"])
    ax.set_title(ttl, fontsize=10.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
a.set_ylim(90, 96); b.set_ylim(0, 13)
save(fig, 2, data="04-code/ch52/output/rerun.txt")
