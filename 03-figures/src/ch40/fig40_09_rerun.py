"""Figure 40.9: rerun agreement on loss_location, 400 decisions in each case."""
from _common import S, save, text, nums
rows = [l for l in text("rerun").split("RERUN AGREEMENT")[1].splitlines()[1:] if "agree" in l]
v = [nums(l.split("agree")[1])[0] for l in rows]
assert v == [397, 285, 398]
labs = ["before hotfix,\nrerun with A", "after hotfix,\nrerun with A", "after hotfix,\nrerun with B"]
fig, ax = S.figure(height=3.8)
cols = [S.ROLE["system"], S.ROLE["blocker"], S.ROLE["system"]]
ax.bar(range(3), [x / 4 for x in v], 0.55, color=cols)
for i, x in enumerate(v):
    ax.text(i, x / 4 + 1.5, f"{x / 4:.1f}%", ha="center", fontsize=10)
ax.set_xticks(range(3)); ax.set_xticklabels(labs); ax.set_ylim(0, 112); ax.set_ylabel("rerun agrees with record (%)")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 9, data="04-code/ch40/output/rerun.txt")
