"""Figure 15.10: the claims-core request against the escalation thresholds and the work it blocks."""
from _common import S, save
from fieldkit.histories import caldwell_policy
pol = caldwell_policy(); sla = pol.sla["shadowed"]; start = 5
fig, ax = S.figure(height=3.8)
ax.barh(2, 54 - start, left=start, height=0.5, color=S.TINT["blocker"], hatch=S.HATCH["blocker"], edgecolor=S.ROLE["blocker"], lw=S.LW["data"])
ax.barh(2, 61 - 54, left=54, height=0.5, color=S.TINT["approval"], edgecolor=S.ROLE["approval"], lw=S.LW["data"])
for d, t in [(start + sla, "level 1 due"), (start + sla + 14, "level 2 due"), (start + 2 * sla, "level 3 due")]:
    ax.axvline(d, color=S.PAL["grey"], lw=S.LW["data"], ls="--"); ax.text(d + 0.5, 3.05, f"{t}\nday {d}", fontsize=9.5, color=S.PAL["ink"], va="top")
for d, t, x, y, ha in [(47, "dated ask\nto Reyes", 41, 1.1, "right"), (49, "board\nbooked", 49, 0.5, "center"),
                      (54, "board\napproves", 57, 1.1, "left")]:
    ax.plot([d], [2], marker="o", color=S.ROLE["evidence"], ms=7, zorder=4)
    ax.annotate(t, (d, 2), xytext=(x, y), ha=ha, va="center", fontsize=9.5, color=S.PAL["ink"],
                arrowprops=dict(arrowstyle="-", color=S.PAL["ink"], lw=S.LW["data"]))
for i, (name, d) in enumerate(sorted(pol.plan.items(), key=lambda kv: kv[1])):
    ax.plot([d], [-0.4], marker="v", color=S.ROLE["cost"], ms=8)
    ax.text(d, -0.75 - 0.5 * (i % 2), f"{name}, day {d}", ha="center", va="top", fontsize=9.5, color=S.PAL["ink"])
ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_xlim(0, 75); ax.set_ylim(-1.9, 3.2); ax.set_xlabel("engagement day")
ax.text(start, 2.42, "claims-core read-only request", fontsize=9.5, color=S.PAL["ink"])
save(fig, 10, data="04-code/fieldkit histories (caldwell_history, caldwell_policy)")
