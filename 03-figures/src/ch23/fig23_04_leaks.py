"""Figure 23.4: 450 searches as an adjuster under three permission modes (acl_inherit.txt)."""
from _common import S, save, text, nums
L = [l for l in text("acl_inherit").splitlines() if l.startswith(("no permission", "filter after", "filter before"))]
vals = [nums(l.split(")")[-1] if ")" in l else l)[-4:] for l in L]
labels = ["no filter", "filter after\nranking", "filter before\nranking"]
fig, ax = S.figure(height=3.9)
w = 0.26; cols = [("searches leaking", S.ROLE["blocker"], 0), ("short lists", S.ROLE["data"], 2), ("empty lists", S.ROLE["cost"], 3)]
for j, (name, c, idx) in enumerate(cols):
    for i, v in enumerate(vals):
        x = i + (j - 1) * w; ax.bar(x, v[idx], w, color=c, label=name if i == 0 else None)
        ax.text(x, v[idx] + 3, f"{int(v[idx])}", ha="center", fontsize=9.5, color=S.PAL["ink"])
ax.set_xticks(range(3), labels); ax.set_ylabel("of 450 searches"); ax.set_ylim(0, 200)
ax.legend(loc="upper right", fontsize=9.5, frameon=False); ax.spines[["top", "right"]].set_visible(False)
save(fig, 4, data="04-code/ch23/output/acl_inherit.txt")
