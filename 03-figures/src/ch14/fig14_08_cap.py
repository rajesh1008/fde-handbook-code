"""Figure 14.8: three answers to the fax path, by pilot day and by spend against the T&M cap."""
from _common import S, save, plt
import pipeline as pl, projection as pj
from day_five import fdes_to_hold

both = pl.ELECTRONIC + pl.FAX
n = fdes_to_hold(both)
rows = [("A: absorb,\n2 FDEs", pj.project(both)), (f"B: absorb, hold\ndate, {n} FDEs", pj.project(both, pj.with_(fdes=n))),
        ("C: carve out,\nowner + date", pj.project(pl.ELECTRONIC))]
fig, (a1, a2) = S.figure(3.9, ncols=2)
roles = ["blocker", "cost", "approval"]
for k, (lab, p) in enumerate(rows):
    a1.barh(k, p["pilot"], height=0.5, color=S.TINT[roles[k]], edgecolor=S.ROLE[roles[k]], hatch=S.HATCH[roles[k]], lw=1.2)
    a1.text(p["pilot"] + 5, k, str(p["pilot"]), va="center", fontsize=10)
    a2.barh(k, p["cost"] / 1e3, height=0.5, color=S.TINT[roles[k]], edgecolor=S.ROLE[roles[k]], hatch=S.HATCH[roles[k]], lw=1.2)
    a2.text(p["cost"] / 1e3 - 8, k, f"\\${p['cost'] / 1e3:,.0f}k", va="center", ha="right", fontsize=10, bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
for a in (a1, a2):
    a.set_yticks(range(3)); a.invert_yaxis()
a1.set_yticklabels([r[0] for r in rows], fontsize=9); a2.set_yticklabels([])
a1.set_xlim(0, 320); a1.set_xlabel("projected pilot day")
a2.axvline(pj.CAP / 1e3, color=S.PAL["ink"], lw=S.LW["emphasis"]); a2.text(pj.CAP / 1e3 + 6, -0.55, "cap \\$450k", ha="left", fontsize=9.5)
a2.set_xlim(0, 600); a2.set_ylim(2.5, -0.8); a1.set_ylim(2.5, -0.8); a2.set_xlabel("build cost at \\$260 an hour, thousands")
save(fig, 8)
