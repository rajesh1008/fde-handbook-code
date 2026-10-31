"""Figure 36.5: the same twenty v3 runs scored by the action oracle and by the canary oracle."""
from _common import S, save, text, blank
from matplotlib.patches import Rectangle
act = [l.split()[-1] for l in text("campaign-v3-action").splitlines() if l.startswith("RT-")]
can = [l[34:42].strip() for l in text("campaign-v3").splitlines() if l.startswith("RT-")]
assert act.count("stopped") == 20 and can.count("reached") == 1
fig, ax = S.figure(height=3.8); blank(ax, (-4.2, 20.2), (-1.4, 4.2))
for row, (vals, bad, name) in enumerate([(act, "ESCAPED", "action oracle"), (can, "reached", "canary oracle")]):
    y = 2.2 - row * 2.2
    for i, v in enumerate(vals):
        r = "blocker" if v == bad else "approval"
        ax.add_patch(Rectangle((i, y), 0.86, 1.2, facecolor=S.ROLE[r] if v == bad else S.TINT[r], edgecolor=S.ROLE[r], lw=1))
    ax.text(-0.3, y + 0.6, name, ha="right", va="center", fontsize=10)
    n = sum(v != bad for v in vals)
    ax.text(20.1, y + 0.6, f"{n}/20", ha="left", va="center", fontsize=10)
ax.text(6.43, -1.0, "RT-07", ha="center", fontsize=9.5)
ax.set_xlim(-4.2, 21.6)
save(fig, 5, data="04-code/ch36/output/campaign-v3-action.txt, campaign-v3.txt")
