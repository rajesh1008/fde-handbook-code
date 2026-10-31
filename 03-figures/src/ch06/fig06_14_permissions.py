"""Figure 6.14: steps the automation needs against the roles that hold each permission today."""
from _common import S, plt, save
from matplotlib.patches import Rectangle
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import permissions as P
roles = list(P.ROLES); steps = P.STEPS
short = {"intake clerk": "intake\nclerk", "senior adjuster": "senior\nadjuster", "underwriting service desk": "underwriting\ndesk",
         "legal mail coordinator": "legal\nmail", "finance cage": "finance\ncage"}
sname = ["read document", "policy by number", "policy by name", "attach to claim", "attorney letters", "finance mail",
         "create claim"]
fig, ax = S.figure(4.2)
for i, s in enumerate(steps):
    for j, r in enumerate(roles):
        ok = all(n in P.ROLES[r] for n in s.needs)
        gap = j == 0 and not ok
        fc = S.TINT["approval"] if ok else (S.TINT["blocker"] if gap else "white")
        ec = S.ROLE["approval"] if ok else (S.ROLE["blocker"] if gap else S.PAL["light"])
        ax.add_patch(Rectangle((j, i), 0.92, 0.85, facecolor=fc, edgecolor=ec, lw=S.LW["control"] if j == 0 else S.LW["data"],
                               hatch="\\\\" if gap else ""))
        t = "holds" if ok else ("gap" if gap else "")
        if t:
            ax.text(j + 0.46, i + 0.43, t, ha="center", va="center", fontsize=9,
                    bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none") if gap else None)
ax.set_xlim(0, len(roles)); ax.set_ylim(len(steps), 0)
ax.set_xticks([j + 0.46 for j in range(len(roles))]); ax.set_xticklabels([short[r] for r in roles], fontsize=9)
ax.xaxis.tick_top()
ax.set_yticks([i + 0.43 for i in range(len(steps))]); ax.set_yticklabels(sname)
for sp in ax.spines.values(): sp.set_visible(False)
ax.tick_params(length=0)
save(fig, 14)
