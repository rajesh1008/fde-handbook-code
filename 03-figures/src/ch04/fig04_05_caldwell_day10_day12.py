"""Figure 4.5: Caldwell's 25 proofs on day 10 and day 12. One must-pass proof moved to held, one to partial."""
from _common import S, save, title, blank, DIMS
from matplotlib.patches import Rectangle
from checklists import caldwell

fig, ax = blank(4.6)
ax.set_xlim(0, 10.6); ax.set_ylim(-1.9, 6.4)
days = (10, 12)
states = {}
for d in days:
    c = caldwell(day=d); v = c.assess(d)
    states[d] = ({k: (p.dimension, p.must_pass, p.counted(c.customer_people)) for k, p in c.proofs.items()},
                 len(v.blocking), v.gated)
changed = {k for k in states[10][0] if states[10][0][k][2] != states[12][0][k][2]}
FILL = dict(held=(S.ROLE["approval"], ""), partial=(S.TINT["data"], ".."), missing=("white", ""))
for j, d in enumerate(days):
    x0 = 3.2 + j * 3.8
    S.label(ax, x0 + 1.5, 5.75, f"day {d}", fs=11, ha="center", weight="bold")
    S.label(ax, x0 + 1.5, 5.25, f"gated {states[d][2]:.2f}, {states[d][1]} blocking", fs=9.5, ha="center")
    for r, dim in enumerate(DIMS):
        keys = [k for k, s in states[d][0].items() if s[0] == dim]
        y = 4.0 - r * 0.95
        if j == 0:
            S.label(ax, 3.0, y + 0.35, dim, fs=10, ha="right", va="center")
        for i, k in enumerate(keys):
            _, must, st = states[d][0][k]
            fc, hat = FILL[st]
            emph = d == 12 and k in changed
            ax.add_patch(Rectangle((x0 + i * 0.62, y), 0.52, 0.7, facecolor=fc, hatch=hat,
                                   edgecolor=S.PAL["ink"] if (must or emph) else S.PAL["grey"],
                                   lw=S.LW["emphasis"] if emph else (S.LW["control"] if must else S.LW["data"])))
# legend
lx = 0.4
for st, txt in (("held", "held"), ("partial", "partial"), ("missing", "missing")):
    fc, hat = FILL[st]
    ax.add_patch(Rectangle((lx, -1.15), 0.4, 0.5, facecolor=fc, hatch=hat, edgecolor=S.PAL["ink"], lw=S.LW["data"]))
    S.label(ax, lx + 0.55, -0.9, txt, fs=9.5, va="center"); lx += 1.75
ax.add_patch(Rectangle((lx, -1.15), 0.4, 0.5, facecolor="white", edgecolor=S.PAL["ink"], lw=S.LW["control"]))
S.label(ax, lx + 0.55, -0.9, "must-pass", fs=9.5, va="center"); lx += 2.0
ax.add_patch(Rectangle((lx, -1.15), 0.4, 0.5, facecolor="white", edgecolor=S.PAL["ink"], lw=S.LW["emphasis"]))
S.label(ax, lx + 0.55, -0.9, "moved", fs=9.5, va="center")
title(ax, "Two days, two proofs moved")
save(fig, 5, kind="diagram", data="04-code/ch04/checklists.caldwell(day=10) and caldwell(day=12)")
