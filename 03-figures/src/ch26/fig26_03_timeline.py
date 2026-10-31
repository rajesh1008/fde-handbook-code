"""Figure 26.3: building and using gold-set-300, days 59 to 95 (engagement plan; lab stand-in)."""
from _common import S, save
rows = [("plan signed", 59, 59, "approval"), ("calibration", 64, 66, "evidence"), ("labeling", 67, 83, "data"),
        ("adjudication", 84, 86, "evidence"), ("first scoring", 87, 87, "model"), ("judge rebuilt", 88, 93, "system"),
        ("gate on p7", 93, 94, "approval"), ("decision D-07", 95, 95, "blocker")]
fig, ax = S.figure(height=3.8)
for i, (lab, a, b, r) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.barh(y, b - a + 0.8, left=a - 0.4, color=S.ROLE[r], hatch=S.HATCH[r], edgecolor="white", height=0.55)
    ax.text(58, y, lab, ha="right", va="center", fontsize=10, color=S.PAL["ink"])
ax.set_yticks([]); ax.set_xlim(46, 97); ax.set_xticks([59, 64, 67, 84, 87, 93, 95])
ax.set_xlabel("engagement day")
ax.spines[["top", "right", "left"]].set_visible(False)
save(fig, 3, kind="diagram", data="engagement plan, Chapter 26")
