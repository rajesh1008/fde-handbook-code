"""Figure 50.14: agreement per accounting standard with 95% intervals against the 90% bar."""
import re
from _common import S, save, text, bar_style
t = text("shadow")
rows = [("all 600", *map(float, re.search(r"= ([\d.]+)% \(95% interval ([\d.]+)% to ([\d.]+)%", t).groups()))]
for s in ("IFRS", "ASPE", "US GAAP"):
    m = re.search(rf"^{s}\s+(\d+)\s+(\d+)\s+([\d.]+)%\s+([\d.]+)% to ([\d.]+)%", t, re.M)
    rows.append((f"{s} {m.group(2)}", float(m.group(3)), float(m.group(4)), float(m.group(5))))
fig, ax = S.figure(height=3.8)
for i, (n, r, lo, hi) in enumerate(rows[::-1]):
    ok = lo >= 90 or r >= 90
    c = S.ROLE["approval"] if r >= 90 else S.ROLE["data"]
    ax.plot([lo, hi], [i, i], color=c, lw=S.LW["emphasis"]); ax.plot([r], [i], "o" if r >= 90 else "s", color=c, ms=7)
    ax.text(hi + 0.4, i, f"{r:.1f}%", va="center", fontsize=9.5)
ax.axvline(90, color=S.PAL["ink"], lw=S.LW["control"], ls="--"); ax.text(90.2, len(rows) - 0.55, "bid bar 90%", fontsize=9.5)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]]); ax.set_xlim(76, 100)
ax.set_xlabel("agreement with the officer's memo, % (95% interval)"); ax.set_ylim(-0.6, len(rows) - 0.2); bar_style(ax)
save(fig, 14, data="04-code/ch50/output/shadow.txt")
