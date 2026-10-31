"""Figure 29.4: layer-one rule cases failing on PR #231, the date-library bump, by rule family (Listing 29.3)."""
from _common import S, save, js
d = js("rules")
fam = d["fam"]; by = d["by"]
fig, ax = S.figure(height=3.9)
names = list(fam)
for i, n in enumerate(names):
    ax.barh(i, fam[n], height=0.6, color=S.TINT["evidence"], edgecolor=S.ROLE["evidence"])
    f = by.get(n, 0)
    if f:
        ax.barh(i, f, height=0.6, color=S.ROLE["blocker"])
    S.label(ax, fam[n] + 1, i, f"{f} of {fam[n]} fail", va="center", fs=9)
ax.set_yticks(range(len(names)), names, fontsize=9)
ax.invert_yaxis(); ax.set_xlim(0, 125); ax.set_xlabel("rule cases")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 4, data="04-code/ch29/output/rules.json")
