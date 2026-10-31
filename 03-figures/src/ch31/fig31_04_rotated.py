"""Figure 31.4: legibility against C06 confidence, rotated faxes before and after the fix (agent.py stand-in)."""
from _common import S, save
from agent import Release, Gateway, run, rotated_faxes, Doc
pts = {"before": [], "after": [], "clean": []}
for lab, rel in (("before", Release(orientation=False, legibility_gate=False)), ("after", Release(legibility_gate=False))):
    for d in rotated_faxes():
        tr, _ = run(d, rel, Gateway())
        leg = float(tr[0][3].split()[-1]); conf = float(tr[1][3].split()[-1])
        pts[lab].append((leg, conf))
for i in range(40):
    tr, _ = run(Doc(f"CL-{i}", 145, "fax", "T1", f"K{i}", truth=dict(date_received="x", policy_number="x"), narrative=False),
                Release(), Gateway())
    pts["clean"].append((float(tr[0][3].split()[-1]), float(tr[1][3].split()[-1])))
fig, ax = S.figure(height=4.0)
style = dict(before=("blocker", "x"), after=("system", "o"), clean=("evidence", "s"))
lbl = dict(before="rotated, pre-fix build", after="rotated, orientation fixed", clean="upright faxes")
for k, v in pts.items():
    ax.scatter([a for a, _ in v], [b for _, b in v], color=S.ROLE[style[k][0]], marker=style[k][1], s=30, label=lbl[k])
ax.axvline(0.5, color=S.PAL["ink"], lw=1.2, ls="--"); S.label(ax, 0.52, 0.995, "CW-I-01: below 0.50, no model call", fs=9, va="top")
ax.set_xlim(0, 1.02); ax.set_ylim(0.9, 1.0); ax.set_xlabel("page legibility after capture"); ax.set_ylabel("C06 confidence")
ax.legend(loc="lower left", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 4, data="04-code/ch31/agent.py rotated_faxes, 24 + 40 stand-in faxes")
