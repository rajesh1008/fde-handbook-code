"""Figure 29.9: PR #212 by document class, prompt p8.3 against p9 on gold-set-300 test (Listing 29.6)."""
from _common import S, save, js
d = js("failure_injection")
rows = d["rows"]
fig, ax = S.figure(height=4.2)
names = list(rows)
for i, n in enumerate(names):
    N, b, a, g, l, v = rows[n]
    pb, pa = 100 * b / N, 100 * a / N
    col = S.ROLE["blocker"] if v == "fail" else S.ROLE["approval"]
    ax.plot([pb, pa], [i, i], color=col, lw=S.LW["emphasis"] if v == "fail" else S.LW["control"])
    ax.plot(pb, i, "o", color=S.PAL["grey"], ms=6); ax.plot(pa, i, "o", color=col, ms=7)
    S.label(ax, max(pb, pa) + 0.6, i, f"{pb:.1f} to {pa:.1f}" + ("  fail" if v == "fail" else ""), va="center", fs=9,
            weight="bold" if v == "fail" else "normal")
wb, wa = d["agg"]
ax.axvline(100 * wb, color=S.PAL["grey"], lw=S.LW["data"], ls="--")
ax.axvline(100 * wa, color=S.ROLE["approval"], lw=S.LW["data"], ls="--")
S.label(ax, 100 * wa + 0.3, -0.75, f"aggregate {100 * wb:.1f} to {100 * wa:.1f}", fs=9)
ax.set_yticks(range(len(names)), names, fontsize=9); ax.set_ylim(len(names) - 0.5, -1.1)
ax.set_xlim(78, 106); ax.set_xlabel("field accuracy (%), grey p8.3, colored p9")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 9, data="04-code/ch29/output/failure_injection.json")
