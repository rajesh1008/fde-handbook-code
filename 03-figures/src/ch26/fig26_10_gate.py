"""Figure 26.10: Caldwell's gate, the four cells for two candidates (Listing 26.5)."""
from _common import S, save, js
d = js("regression_gate")
fig, ax = S.figure(height=3.8)
cands = [("p7", "p7 vs p6"), ("p7+alias", "newer model vs p7")]
for i, (k, lab) in enumerate(cands):
    c = d[k]["cells"]
    ax.bar(i * 3, c["gained"], color=S.ROLE["approval"], width=0.9, label="gained" if i == 0 else None)
    ax.bar(i * 3 + 1, c["lost"], color=S.ROLE["blocker"], hatch=S.HATCH["blocker"], edgecolor="white", width=0.9,
           label="lost" if i == 0 else None)
    ax.text(i * 3, c["gained"] + 5, str(c["gained"]), ha="center", fontsize=10)
    ax.text(i * 3 + 1, c["lost"] + 5, str(c["lost"]), ha="center", fontsize=10)
    ax.text(i * 3 + 0.5, 300, f"{d[k]['wb']:.1%} to {d[k]['wa']:.1%}", ha="center", fontsize=10)
ax.set_xticks([0.5, 3.5], [c[1] for c in cands])
ax.set_ylim(0, 330); ax.set_ylabel("fields that changed (of 3,000)")
ax.legend(loc="center right", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 10, data="04-code/ch26/output/regression_gate.json")
