"""Figure 11.3: naive versus gated map scores for five maps."""
from _common import S, save, plt
import stakeholders as St, greystone as G, caldwell, pennant
maps = [("Greystone d2", G.KICKOFF, None), ("Greystone d12", G.DAY12, None),
        ("Greystone d40", G.at_day(G.DAY12, G.CONTACT_DAY40, 40), None),
        ("Caldwell d25", caldwell.DAY25, None), ("Pennant d28", pennant.DAY28, None)]
fig, ax = S.figure(3.8)
ys = range(len(maps))
for i, (name, m, _) in enumerate(maps):
    n, g = St.naive_score(m), St.gated_score(m)
    ax.barh(i + 0.18, n, height=0.34, color=S.TINT["evidence"], edgecolor=S.ROLE["evidence"], hatch=S.HATCH["evidence"])
    ax.barh(i - 0.18, g, height=0.34, color=S.ROLE["system"], edgecolor="white", hatch=S.HATCH["system"])
    v = St.verdict(m)
    ax.text(1.02, i, v.lower(), va="center", fontsize=9.5, color=S.PAL["ink"])
ax.set_yticks(list(ys)); ax.set_yticklabels([m[0] for m in maps]); ax.invert_yaxis()
ax.set_xlim(0, 1.3); ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0]); ax.set_xlabel("score (share of five roles)")
ax.legend(["naive: a name in the column", "gated: confirmed and in contact"], loc="lower right", fontsize=9.5)
save(fig, 3)
