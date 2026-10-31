"""Figure 34.1: Caldwell's production addendum, day 121 to go-live on day 158 (story calendar, ledger ch34)."""
from _common import S, save, blank
fig, ax = S.figure(height=4.9); blank(ax, (110, 165), (0, 10))
ax.plot([115, 162], [5, 5], color=S.PAL["grey"], lw=1.5)
ev = [(121, 121, "v1 draft\narrives", "data", 1), (136, 129.5, "v3 agreed\nin principle", "blocker", 1),
      (138, 138, "check:\n-8.0%", "blocker", 1), (149, 147, "v5 signed:\n48.7%", "approval", 1),
      (158, 156.5, "go-live", "model", 1), (137, 133, "v0 extractor:\n17.9%", "evidence", -1),
      (146, 142.5, "Exhibit E\nsigned off", "approval", -1), (153, 152, "model-risk\nreview passed", "system", -1)]
for d, cx, t, r, side in ev:
    y = 6.2 if side > 0 else 1.3
    ax.plot([d, cx], [5, y if side > 0 else y + 2.4], color=S.PAL["grey"], lw=0.75)
    S.box(ax, cx - 3.4, y, 6.8, 2.4, t, role=r, fs=9.5)
    ax.plot(d, 5, "o", color=S.ROLE[r], ms=6)
for d in range(115, 165, 5):
    ax.text(d, 3.7, f"{d}", ha="center", fontsize=9, color=S.PAL["ink"])
ax.text(162, 3.1, "day", ha="right", fontsize=9)
ax.annotate("", xy=(146, 4.2), xytext=(139, 4.2), arrowprops=dict(arrowstyle="<->", color=S.ROLE["cost"], lw=1.5))
save(fig, 1, kind="diagram", data="04-code/ch34/output/margin.txt; 00-plan/ledger/ch34.md")
