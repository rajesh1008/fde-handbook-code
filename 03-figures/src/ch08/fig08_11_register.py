"""Figure 8.11: Caldwell's seven open decisions on day 28: raised day, due day and owner."""
from _common import S, plt, save
import caldwell_scope as cs
reg = cs.register()
fig, ax = S.figure(4.2)
owners = {"Daniel Reyes": "model", "Anne Kessler": "approval", "Priya Natarajan": "system"}
for i, d in enumerate(sorted(reg, key=lambda d: d.due_day)):
    r = owners[d.owner]
    ax.plot([d.raised_day, d.due_day], [i, i], color=S.ROLE[r], lw=2.5)
    ax.plot(d.raised_day, i, "o", color=S.ROLE[r]); ax.plot(d.due_day, i, "s", color=S.ROLE[r])
    ax.text(d.due_day + 1.5, i, f"{d.key} {d.owner.split()[0]}, day {d.due_day}", va="center", fontsize=9)
ax.axvline(28, color=S.PAL["ink"], lw=0.75, ls="--"); ax.text(28.8, 6.55, "signed, day 28", fontsize=9)
ax.set_yticks([]); ax.set_xlim(0, 125); ax.set_ylim(-0.7, 7.0)
ax.set_xlabel("engagement day (circle raised, square due)")
for s in ("left",): ax.spines[s].set_visible(False)
save(fig, 11)
