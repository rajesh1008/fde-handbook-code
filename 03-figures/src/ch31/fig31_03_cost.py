"""Figure 31.3: cost per routed document by component (tree.txt)."""
from _common import S, save, text, nums
rows = [l.strip() for l in text("tree").splitlines() if l.startswith("  ") and "$" in l and "total" not in l and l.strip()[:3] != "all"]
SHORT = ["OCR, C01", "C06 prompted, c06-p4", "C07 small model", "C11 frontier", "retrieval", "router, guards, logs", "review labor", "escalation labor"]
names = SHORT[:len(rows)]; vals = [nums(r.rsplit("$", 1)[1])[0] for r in rows]
fig, ax = S.figure(height=4.2)
for i, (n, v) in enumerate(zip(names, vals)):
    role = "cost" if "labor" in n else "system"
    ax.barh(i, v, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white")
    S.label(ax, v + 0.004, i, f"${v:.4f}", fs=9, va="center")
ax.set_yticks(range(len(names)), names, fontsize=9); ax.invert_yaxis(); ax.set_xlim(0, 0.30)
ax.set_xlabel("dollars per routed document (stand-in rates, $46/hour)")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 3, data="04-code/ch31/output/tree.txt")
