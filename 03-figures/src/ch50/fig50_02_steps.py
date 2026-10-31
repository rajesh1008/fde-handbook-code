"""Figure 50.2: who does each of the twenty memo steps; code and tables first, models last, people decide."""
from collections import Counter
from _common import S, save, W, bar_style
ORDER = [("code", "system"), ("reference table", "evidence"), ("small model, checked by code", "data"),
         ("model drafts, cited", "model"), ("person", "approval")]
secs = list(dict.fromkeys(s[0] for s in W.STEPS))
fig, ax = S.figure(height=4.2)
for i, sec in enumerate(secs[::-1]):
    c = Counter(s[2] for s in W.STEPS if s[0] == sec); x = 0
    for who, role in ORDER:
        n = c.get(who, 0)
        if n:
            ax.barh(i, n, left=x, color=S.TINT[role], edgecolor=S.ROLE[role], lw=S.LW["control"], hatch=S.HATCH[role])
            x += n
ax.set_yticks(range(len(secs))); ax.set_yticklabels(secs[::-1]); ax.set_xlabel("steps")
ax.set_xlim(0, 11.5); bar_style(ax)
from matplotlib.patches import Patch
tot = Counter(s[2] for s in W.STEPS)
ax.legend([Patch(fc=S.TINT[r], ec=S.ROLE[r], hatch=S.HATCH[r]) for _, r in ORDER], [f"{w} ({tot[w]})" for w, _ in ORDER],
          loc="center right", fontsize=9)
save(fig, 2, data="04-code/ch50/world.py STEPS")
