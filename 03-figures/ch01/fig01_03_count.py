"""Figure 1.3: how many FDE jobs there are depends on the definition (sources and dates as labelled)."""
from _common import S, save
import matplotlib.pyplot as plt
rows = [("Other public trackers, same week\n(strict title)", 426, 736, "slate", "late Oct 2026"),
        ("Independent census, live postings\n(strict title, 547 companies)", 1276, 1276, "evidence", "observed 30 Oct 2026"),
        ("Broad customer-embedded\nengineering roles", 18000, 25000, "data", "estimate, late Oct 2026")]
fig, ax = plt.subplots(figsize=(9, 4.2))
for i, (lab, lo, hi, role, when) in enumerate(rows):
    y = len(rows) - 1 - i
    c = S.ROLE[role] if role in S.ROLE else S.PAL[role]
    if lo == hi:
        ax.plot([lo], [y], marker="D", ms=10, color=c)
        txt = f"{lo:,}"
    else:
        ax.plot([lo, hi], [y, y], lw=9, color=c, solid_capstyle="butt", alpha=0.85)
        txt = f"{lo:,}–{hi:,}"
    ax.text(hi * 1.25, y, f"{txt}   ({when})", va="center", fontsize=8.5)
ax.set_xscale("log"); ax.set_xlim(200, 400000)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in reversed(rows)], fontsize=8.5)
ax.set_xlabel("open roles worldwide (log scale)")
ax.set_title("The same week, three answers to 'how many FDE jobs are there'", loc="left", fontsize=11)
ax.text(220, -0.95, "Growth claims use different baselines: about 729% year on year (postings, April 2026);\n"
        "over 1,000% year on year (postings, January-August 2026).", fontsize=7.5, style="italic", color=S.PAL["ink"], va="center")
ax.set_ylim(-1.2, 2.5)
save(fig, 3)
