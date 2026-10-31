"""Figure 8.4: lint findings on scope draft v0.3 (day 24) against the signed v1.0 (day 28), by finding."""
from collections import Counter
from _common import S, plt, save
import caldwell_scope as cs
a = Counter(c for _, c, _ in cs.draft_v03().lint()); b = Counter(c for _, c, _ in cs.signed().lint())
keys = [k for k, _ in a.most_common()]
fig, ax = S.figure(3.9)
for i, k in enumerate(keys):
    ax.barh(i + 0.18, a[k], height=0.34, color=S.ROLE["blocker"], hatch=S.HATCH["blocker"], edgecolor="white")
    ax.barh(i - 0.18, b[k], height=0.34, color=S.ROLE["approval"], edgecolor="white")
    ax.text(a[k] + 0.05, i + 0.18, f"v0.3: {a[k]}", va="center", fontsize=9)
    ax.text(b[k] + 0.05, i - 0.18, f"v1.0: {b[k]}", va="center", fontsize=9)
ax.set_yticks(range(len(keys))); ax.set_yticklabels([k.lower() for k in keys], fontsize=9)
ax.invert_yaxis(); ax.set_xlim(0, 3); ax.set_xticks([0, 1, 2, 3]); ax.set_xlabel("findings")
save(fig, 4)
