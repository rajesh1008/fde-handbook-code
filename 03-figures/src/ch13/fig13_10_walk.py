"""The oldest open record walked forward against the stop rule's deadline (Try It 3)."""
from _common import S, save, plt
from cadence_data import caldwell_register
days = list(range(28, 81))
reg = caldwell_register(); d01 = reg.records["D-01"]
fig, ax = S.figure(3.9)
ax.plot(days, [d01.age(d) for d in days], color=S.ROLE["blocker"], lw=S.LW["emphasis"])
ax.axvline(33, color=S.PAL["ink"], ls=":", lw=S.LW["control"]); ax.text(33.5, 8, "due day 33", fontsize=9)
ax.axvline(75, color=S.PAL["ink"], ls="--", lw=S.LW["control"]); ax.text(74.5, 8, "stop-rule\ndeadline day 75", ha="right", fontsize=9)
ax.axvline(56, color=S.PAL["grey"], lw=S.LW["data"]); ax.text(56.5, 62, "day 56: 51 days", fontsize=9)
ax.set_xlabel("engagement day"); ax.set_ylabel("days D-01 has been open")
ax.set_xlim(28, 80); ax.set_ylim(0, 80)
save(fig, 10)
