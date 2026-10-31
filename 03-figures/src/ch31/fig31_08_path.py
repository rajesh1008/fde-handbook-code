"""Figure 31.8: Caldwell accuracy across the engagement (style sheet canon; rc-1 from scorecard.txt)."""
from _common import S, save, text, nums
rc1 = nums([l for l in text("scorecard").splitlines() if l.startswith("all fields")][0])[5]
pts = [("Northlight\nsuite", 91.0), ("Anne's set,\nday 88", 68.4), ("p7 gate,\nday 94", 76.7), ("rc-1,\nday 156", rc1)]
fig, ax = S.figure(height=3.9)
ax.plot(range(4), [p for _, p in pts], color=S.ROLE["model"], lw=2, marker="o")
for i, (_, p) in enumerate(pts):
    S.label(ax, i + 0.08, p + (1.8 if i in (0, 3) else -4.5), f"{p:.1f}%", ha="left", fs=10)
ax.axhline(80, color=S.ROLE["blocker"], ls="--", lw=1.2); S.label(ax, -0.3, 81.0, "draft bar 80%", fs=9)
S.label(ax, 0.05, 61, "first point: our suite; the rest: Anne's set", fs=9)
ax.set_xticks(range(4), [n for n, _ in pts], fontsize=9); ax.set_ylim(58, 98); ax.set_xlim(-0.4, 3.4)
ax.set_ylabel("field accuracy (%)"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 8, data="style sheet Ch26 canon; 04-code/ch31/output/scorecard.txt")
