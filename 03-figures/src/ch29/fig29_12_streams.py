"""Figure 29.12: six verification streams on 235 wrong fields, before and after the second pass moved to another pin (Listing 29.8)."""
from _common import S, save, js
d = js("streams")
keys = list(d)
fig, axes = S.figure(height=4.2, ncols=2, sharey=True)
for ax, k, t in zip(axes, keys, ("day 140: same model", "day 148: different pin")):
    rows = d[k]["rows"]; names = list(rows)
    for i, n in enumerate(names):
        ax.barh(i, rows[n]["caught"], height=0.6, color=S.TINT["evidence"], edgecolor=S.ROLE["evidence"])
        ax.barh(i, rows[n]["unique"], height=0.6, color=S.ROLE["model"])
        S.label(ax, rows[n]["caught"] + 2, i, f"{rows[n]['unique']} only", va="center", fs=9)
    ax.set_xlim(0, 175); ax.set_xlabel("wrong fields caught")
    ax.set_title(f"{t}: any {d[k]['union']} of {d[k]['n']}", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_yticks(range(6), [n.replace(" ", "\n", 1) for n in d[keys[0]]["rows"]], fontsize=9); axes[0].invert_yaxis()
save(fig, 12, data="04-code/ch29/output/streams.json")
