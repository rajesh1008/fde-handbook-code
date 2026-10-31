"""Figure 32.5: Greystone's 19 evidence items from issue to expiry, against the review and pilot days."""
from _common import S, save, world
from fieldkit.security import reuse
ev = sorted(world.EVIDENCE.values(), key=lambda e: e.expires_day)
use = reuse(world.ANSWERS)
fig, ax = S.figure(height=5.6)
lo, hi = -330, 330
for i, e in enumerate(ev):
    bad = e.expires_day <= world.REVIEW_DAY or e.scope not in ("any", world.SCOPE) or not __import__("fieldkit.security", fromlist=["x"]).is_person(e.owner)
    r = "blocker" if bad else "evidence"
    ax.barh(i, min(e.expires_day, hi) - max(e.issued_day, lo), left=max(e.issued_day, lo), height=0.6,
            color=S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r])
    ax.text(lo - 8, i, e.id, ha="right", va="center", fontsize=9, family="monospace")
    ax.text(min(e.expires_day, hi) + 5, i, f"{use[e.id]}", va="center", fontsize=9)
for d, nm, ha in ((world.REVIEW_DAY, "review 103", "right"), (131, "pilot 131", "left")):
    ax.axvline(d, color=S.PAL["ink"], lw=S.LW["control"], ls="--")
    ax.text(d + (-4 if ha == "right" else 4), -0.6, nm, ha=ha, fontsize=9)
ax.set_yticks([]); ax.set_xlim(lo - 60, hi + 30); ax.invert_yaxis(); ax.set_ylim(len(ev) - 0.4, -1.2)
ax.set_xlabel("engagement day (negative: before the engagement)")
ax.text(hi + 25, -0.6 + 0.0, "answers", ha="right", fontsize=9)
ax.spines[["top", "right", "left"]].set_visible(False)
save(fig, 5, data="04-code/ch32/world.py EVIDENCE; output/evidence_map.txt")
