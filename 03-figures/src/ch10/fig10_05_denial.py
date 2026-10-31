"""Figure 10.5: what the denied API cost Pennant's estimate: day 21 total, the assumed line removed, the five
lines of the CSV path added, day 24 total."""
from _common import S, plt, save, quiet
with quiet():
    from inventories import pennant
d21, d24 = pennant(denied=False), pennant()
alt = [l for l in d24.lines if l.lid.startswith("P-T")]
steps = [("day 21", d21.total(), "total")] + [("API line", -40, "minus")] + [(l.lid, l.likely, "plus") for l in alt] + [("day 24", d24.total(), "total")]
fig, ax = S.figure(3.8); run = 0
for i, (name, v, kind) in enumerate(steps):
    if kind == "total":
        ax.bar(i, v, color=S.TINT["evidence"], edgecolor=S.ROLE["evidence"], hatch="xx", width=0.6); run = v; top = v
    else:
        base = run + min(v, 0); r = "approval" if v < 0 else "blocker"
        ax.bar(i, abs(v), bottom=base, color=S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r] or None, width=0.6); run += v; top = run if v > 0 else run + abs(v)
    ax.text(i, top + 25, f"{v:+,.0f}" if kind != "total" else f"{v:,.0f}", ha="center", fontsize=9)
ax.set_xticks(range(len(steps))); ax.set_xticklabels([s[0] for s in steps], fontsize=9, rotation=30, ha="right")
ax.set_ylabel("most-likely integration hours"); ax.set_ylim(0, 1750)
save(fig, 5)
