"""Figure 6.9: known volume and covered volume over the fortnight."""
from _common import S, plt, save
from caldwell_discovery import build_log
log = build_log(); days = list(range(9, 27))
kv = [log.coverage(d).total_volume for d in days]; cv = [log.coverage(d).covered_volume for d in days]
fig, ax = S.figure(3.8)
ax.step(days, kv, where="post", color=S.ROLE["data"], lw=S.LW["emphasis"], ls="--")
ax.step(days, cv, where="post", color=S.ROLE["approval"], lw=S.LW["emphasis"])
ax.text(9.2, 9700, "volume known", fontsize=9.5, color=S.PAL["ink"])
ax.text(14.2, 5600, "volume covered", fontsize=9.5, color=S.PAL["ink"])
ax.axhline(14800, color=S.PAL["grey"], lw=S.LW["data"], ls=":")
ax.text(19.5, 15200, "14,800 a month by day 26", fontsize=9)
ax.set_xlabel("engagement day"); ax.set_ylabel("documents a month"); ax.set_ylim(0, 16500)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
save(fig, 9)
