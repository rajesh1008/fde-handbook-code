"""Figure 34.6: probability that a month is in breach, by true error rate, for three ways to write the same level."""
from _common import S, save
from fieldkit.contract import point_rule, design_service_level
fig, ax = S.figure(height=4.8)
xs = [i / 1000 for i in range(2, 51)]
rules = [("point rule, n 400, above 1.0%", point_rule("c", "e", "s", .01, .03, 400, .010), "blocker", "-"),
         ("point rule, n 400, above 2.0%", point_rule("c", "e", "s", .01, .03, 400, .020), "data", "--"),
         ("designed, n 310, 7 or more errors", design_service_level("c", "e", "s", .01, .03), "approval", "-")]
for lab, r, role, ls in rules:
    ax.plot([100 * x for x in xs], [100 * r.p_breach(x) for x in xs], color=S.ROLE[role], lw=2.5 if role == "approval"
            else 1.5, ls=ls, label=lab)
ax.axvline(0.9, color=S.PAL["grey"], lw=0.75); ax.text(1.0, 50, "Caldwell now: 0.9%", fontsize=9.5)
ax.set_xlabel("true post-review error rate (%)"); ax.set_ylabel("chance a month is in breach (%)")
ax.set_xlim(0, 5); ax.set_ylim(0, 100); ax.legend(fontsize=9.5, loc="lower right")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 6, data="04-code/ch34/output/sl.txt (rules recomputed with fieldkit.contract)")
