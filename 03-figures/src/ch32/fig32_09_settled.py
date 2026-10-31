"""Figure 32.9: when Greystone's 23 design-changing answers were settled."""
from _common import S, save, world
d = sorted(world.SETTLED)
fig, ax = S.figure(height=3.9)
xs = [0] + d + [110]; ys = [0] + list(range(1, len(d) + 1)) + [len(d)]
ax.step(xs, ys, where="post", color=S.ROLE["model"], lw=S.LW["emphasis"])
for day, nm in ((40, "clinics end"), (89, "four changes"), (103, "review")):
    ax.axvline(day, color=S.PAL["grey"], lw=0.75, ls="--")
    ax.text(day - 1.5, 24.2, nm, ha="right", fontsize=9)
ax.text(42, sum(x <= 40 for x in d) - 2.5, f"{sum(x <= 40 for x in d)} by day 40", fontsize=9)
ax.text(96, 12.5, f"{sum(x > 40 for x in d)} after day 40", fontsize=9, ha="right")
ax.set_xlabel("engagement day"); ax.set_ylabel("design-changing answers settled"); ax.set_ylim(0, 26); ax.set_xlim(0, 110)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 9, data="04-code/ch32/world.py SETTLED")
