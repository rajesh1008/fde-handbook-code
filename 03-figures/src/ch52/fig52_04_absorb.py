"""Figure 52.4: of 30 Caldwell work items, the forecast moves 10 into the product and leaves 11 with the FDE."""
from _common import S, save, text
rows = {l.split()[0]: (int(l.split()[1]), int(l.split()[2])) for l in text("absorb").splitlines()
        if l.split() and l.split()[0] in ("product", "playbook", "FDE")}
fig, ax = S.figure(height=3.8)
roles = {"product": "system", "playbook": "data", "FDE": "approval"}
for j, (yr, y) in enumerate((("2026", 1), ("2029 forecast", 0))):
    left = 0
    for o in ("product", "playbook", "FDE"):
        v = rows[o][j]
        ax.barh(y, v, left=left, color=S.TINT[roles[o]], edgecolor=S.ROLE[roles[o]], hatch=S.HATCH[roles[o]],
                lw=S.LW["control"], label=o if j == 0 else None)
        if v >= 4:
            ax.text(left + v / 2, y, f"{o} {v}", ha="center", va="center", fontsize=10,
                    bbox=dict(fc="white", ec="none", pad=1))
        else:
            ax.text(left + v / 2, y + 0.47, f"{o} {v}", ha="center", va="bottom", fontsize=9.5)
        left += v
ax.set_ylim(-0.5, 1.75); ax.set_yticks([1, 0]); ax.set_yticklabels(["2026", "2029 forecast"])
ax.set_xlabel("Work items in the Caldwell engagement"); ax.set_xlim(0, 30)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
save(fig, 4, data="04-code/ch52/output/absorb.txt")
