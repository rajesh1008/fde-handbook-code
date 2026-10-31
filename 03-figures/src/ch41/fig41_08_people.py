"""Figure 41.8: the score if one person leaves: Caldwell spreads its evidence, Pennant leans on Jenna Ruiz."""
from _common import S, save, text
import sys; sys.path.insert(0, str(__import__("_common").R / "04-code/ch41"))
import world as W
from fieldkit.handover import score, without
fig, ax = S.figure(height=4.4)
rows = []
for cust, st, r in (("Caldwell", W.CALDWELL_AFTER, "system"), ("Pennant", W.PENNANT, "data")):
    it = W.items(st); base = score(it).gated
    ppl = sorted({p for i in it for p in i.by}, key=lambda p: score(without(it, p)).gated)[:3]
    rows += [(f"{cust}: {p}", base, score(without(it, p)).gated, r) for p in ppl]
for i, (lab, b, w, r) in enumerate(rows):
    ax.plot([w, b], [i, i], color=S.ROLE[r], lw=S.LW["control"])
    ax.scatter([b], [i], color=S.ROLE[r], s=40); ax.scatter([w], [i], color=S.ROLE["blocker"], marker="D", s=50)
    ax.text(w - 0.02, i, f"{w:.2f}", ha="right", va="center", fontsize=9)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis()
ax.set_xlim(0.2, 1.0); ax.set_xlabel("gated readiness score, before and after one person leaves")
ax.spines[["top", "right"]].set_visible(False)
assert "Jenna Ruiz -0.10 (to 0.30)" in text("readiness_pennant")
save(fig, 8, data="04-code/ch41 world.py; fieldkit/handover.py without(); output/readiness_pennant.txt")
