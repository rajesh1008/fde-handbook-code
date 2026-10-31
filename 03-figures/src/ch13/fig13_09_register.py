"""Caldwell decision register on day 56: age of each record and its due day."""
from _common import S, save, plt
from cadence_data import caldwell_register
reg = caldwell_register(); today = 56
rs = sorted(reg.records.values(), key=lambda r: r.raised_day)
fig, ax = S.figure(3.9)
for y, r in enumerate(rs):
    end = r.decided_day if r.status == "decided" else today
    over = r.status == "open" and today > r.due_day
    role = "blocker" if over else ("approval" if r.status == "decided" else "data")
    ax.barh(y, end - r.raised_day, left=r.raised_day, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white", height=0.6)
    ax.plot(r.due_day, y, marker="|", ms=14, mew=2.5, color=S.PAL["ink"])
    ax.text(max(end, r.due_day) + 1, y, ("overdue " if over else "") + r.kind, va="center", fontsize=9)
ax.axvline(today, color=S.PAL["ink"], ls="--", lw=S.LW["data"])
ax.text(today - 0.5, -0.9, "day 56", ha="right", fontsize=9)
ax.set_yticks(range(len(rs))); ax.set_yticklabels([r.key for r in rs]); ax.invert_yaxis()
ax.set_xlim(0, 80); ax.set_xlabel("engagement day (bar: raised to decided or today; tick: due day)")
save(fig, 9)
