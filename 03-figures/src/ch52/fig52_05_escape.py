"""Figure 52.5: gm-n2 writes 38% fewer summary tokens and drops the dispute statement in 12 of 34 summaries."""
from _common import S, save, text
rows = [l.split() for l in text("escape").splitlines() if l.startswith("gm-") and len(l.split()) == 4]
assert [r[0] for r in rows] == ["gm-2026-05-14", "gm-n1", "gm-n2"]
fig, ax = S.figure(height=4.0)
for i, r in enumerate(rows):
    kept, dropped, tok = int(r[1]), int(r[2]), int(r[3])
    ax.bar(i, kept, color=S.TINT["evidence"], edgecolor=S.ROLE["evidence"], hatch=S.HATCH["evidence"], lw=S.LW["control"],
           label="dispute statement kept" if i == 0 else None)
    ax.bar(i, dropped, bottom=kept, color=S.TINT["blocker"], edgecolor=S.ROLE["blocker"], hatch=S.HATCH["blocker"],
           lw=S.LW["emphasis"], label="dropped" if i == 0 else None)
    ax.text(i, 35.2, f"{tok} tokens", ha="center", fontsize=9.5)
ax.set_xticks(range(3)); ax.set_xticklabels(["pin", "n+1", "n+2"])
ax.set_ylabel("Summaries with a dispute statement"); ax.set_ylim(0, 46)
ax.legend(loc="upper center", ncol=2)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
save(fig, 5, data="04-code/ch52/output/escape.txt")
