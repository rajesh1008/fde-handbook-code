"""Figure 29.3: layer-one run time on the 200 commits of days 141 to 170 (Listing 29.9; stand-in timing model)."""
from _common import S, save, js
d = js("month")
xs = d["l1"]
fig, ax = S.figure(height=3.7)
ax.hist(xs, bins=16, color=S.TINT["system"], edgecolor=S.ROLE["system"], hatch=S.HATCH["system"])
ax.axvline(30, color=S.ROLE["blocker"], lw=S.LW["control"])
S.label(ax, 29.5, ax.get_ylim()[1] * 0.85, "budget 30 s", ha="right", fs=9)
med = sorted(xs)[len(xs) // 2]
ax.axvline(med, color=S.PAL["ink"], lw=S.LW["data"], ls="--")
S.label(ax, med + 0.4, ax.get_ylim()[1] * 0.95, f"median {med:.0f} s", fs=9)
ax.set_xlim(0, 32); ax.set_xlabel("seconds per layer-one run"); ax.set_ylabel("commits")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 3, data="04-code/ch29/output/month.json")
