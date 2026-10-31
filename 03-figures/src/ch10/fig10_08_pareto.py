"""Figure 10.8: cumulative share of Pennant's monthly volume by layouts ranked by volume (seeded stand-in), with
cumulative integration hours; twelve layouts carry 76% of volume."""
from _common import S, plt, save, quiet
with quiet():
    from inventories import PENNANT_KINDS
hrs = []
for kind, n, lo, li, hi in PENNANT_KINDS: hrs += [li] * n
w = [1 / (r ** 1.1) for r in range(1, 42)]; tot = sum(w)
cv, ch, a, b = [], [], 0, 0
for x, h in zip(w, hrs): a += x; b += h; cv.append(100 * a / tot); ch.append(100 * b / sum(hrs))
fig, ax = S.figure(3.8); r = list(range(1, 42))
ax.plot(r, cv, color=S.ROLE["system"], lw=S.LW["emphasis"], label="volume covered")
ax.plot(r, ch, color=S.ROLE["cost"], lw=S.LW["control"], ls="--", label="format hours spent")
ax.axvline(12, color=S.PAL["grey"], lw=S.LW["data"]); ax.plot([12], [cv[11]], marker="o", color=S.PAL["ink"])
ax.text(13, cv[11] - 6, f"12 layouts: {cv[11]:.0f}% of volume,\n{ch[11]:.0f}% of format hours", fontsize=9)
ax.set_xlabel("layouts, ranked by monthly volume"); ax.set_ylabel("cumulative share (%)"); ax.set_ylim(0, 105); ax.set_xlim(0, 42)
ax.legend(fontsize=9, frameon=False, loc="lower right")
save(fig, 8)
