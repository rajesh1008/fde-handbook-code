"""Figure 6.4: the tracer form's two days, almost all of it waiting."""
from _common import S, plt, save
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import tracer as T
ev = T.EVENTS; t0 = ev[0][0]
hrs = [(e[0] - t0).total_seconds() / 3600 for e in ev]
fig, ax = S.figure(3.7)
for k in range(len(ev) - 1):
    ax.barh(0, hrs[k + 1] - hrs[k], left=hrs[k], height=0.5, color=S.TINT["evidence"], edgecolor=S.ROLE["evidence"],
            hatch="xx", lw=S.LW["data"])
worked = [k for k, e in enumerate(ev) if e[4]]
for k, e in enumerate(ev):
    if e[4]:
        j = worked.index(k)
        ax.barh(0, max(e[4] / 60, 0.6), left=hrs[k], height=0.5, color=S.ROLE["system"], zorder=3)
        lvl = (0.45, 0.8, 0.45, 0.8)[j % 4]
        ax.plot([hrs[k], hrs[k]], [0.25, lvl], color=S.PAL["ink"], lw=S.LW["data"])
        ax.text(hrs[k], lvl + 0.02, f"{e[1]}, {e[4]} min", fontsize=9, ha="left" if j == 0 else ("right" if j == len(worked) - 1 else "center"), va="bottom")
ax.set_yticks([]); ax.set_ylim(-0.6, 1.2)
ax.set_xlabel("hours after the fax was sent"); ax.set_xlim(-2, 58)
ax.text(28, -0.45, "hatched: waiting in a queue or mailbox; solid: hands on", ha="center", fontsize=9)
for s in ("left", "top", "right"): ax.spines[s].set_visible(False)
save(fig, 4)
