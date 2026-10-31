"""Figure 50.15: why the sample went from 400 to 600 memos; the US GAAP interval at each size."""
import re
from _common import S, save, text, bar_style
t = text("shadow"); rows = []
for total in (400, 600):
    line = next(l for l in t.splitlines() if l.strip().startswith(f"{total} memos"))
    for s, k, n, lo, hi in re.findall(r"(IFRS|ASPE|US GAAP) (\d+)/(\d+) ([\d.]+)% to ([\d.]+)%", line):
        rows.append((total, s, int(n), float(lo), float(hi)))
fig, ax = S.figure(height=3.9)
labels = []
for i, (total, s, n, lo, hi) in enumerate(rows):
    y = len(rows) - 1 - i - (0.5 if total == 600 else 0)
    c = S.ROLE["data"] if total == 400 else S.ROLE["evidence"]
    ax.plot([lo, hi], [y, y], color=c, lw=S.LW["emphasis"], ls="-" if total == 600 else (0, (4, 2)))
    ax.text(hi + 0.4, y, f"{hi - lo:.1f} pts", va="center", fontsize=9.5); labels.append((y, f"{s}, {n} of {total}"))
ax.axvline(90, color=S.PAL["ink"], lw=S.LW["control"], ls="--")
ax.set_yticks([y for y, _ in labels]); ax.set_yticklabels([l for _, l in labels], fontsize=9.5); ax.set_xlim(70, 100)
ax.set_xlabel("95% interval on agreement, % (dashed: 400-memo plan)"); bar_style(ax)
save(fig, 15, data="04-code/ch50/output/shadow.txt")
