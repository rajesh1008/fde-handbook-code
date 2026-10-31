"""Figure 50.1: twelve document formats in 638 credit packages, across three accounting standards."""
from _common import S, save, W, bar_style
names = [n for n, _ in W.FORMATS][::-1]; vals = [v for _, v in W.FORMATS][::-1]
gen = {"facility agreement", "relationship manager call notes", "prior credit memo", "RM call notes"}
fig, ax = S.figure(height=4.6)
for i, (n, v) in enumerate(zip(names, vals)):
    role = "evidence" if any(g in n for g in gen) else "data"
    ax.barh(i, v, color=S.TINT[role], edgecolor=S.ROLE[role], lw=S.LW["control"], hatch=S.HATCH[role])
    ax.text(v + 15, i, f"{v:,}", va="center", fontsize=9.5)
ax.set_yticks(range(len(names))); ax.set_yticklabels(names, fontsize=9.5)
ax.set_xlabel("documents in the 638 packages"); ax.set_xlim(0, 1400); bar_style(ax)
p = W.PACKAGES
ax.text(1380, 11.3, "packages by standard\n" + "\n".join(f"{k} {v}" for k, v in p.items()), ha="right", va="top", fontsize=9.5)
save(fig, 1, data="04-code/ch50/world.py FORMATS, PACKAGES")
