"""Figure 19.15: reconciliation of the 152 first notices against the next morning's extract."""
import re
from _common import S, save, text, dct
t = text("reconcile_caldwell")
fixed = dct(re.search(r"first notices 152: reconciliation (\{.*?\})", t).group(1))
first = dct(re.search(r"first build.*?(\{.*?\})", t).group(1))
fig, ax = S.figure(height=3.9)
keys = [("matched", "approval"), ("held", "evidence"), ("missing", "blocker"), ("extra", "cost"),
        ("mismatched", "data")]
for i, rec in enumerate([first, fixed]):
    left = 0
    for k, r in keys:
        v = rec.get(k, 0)
        ax.barh(i, v, left=left, color=S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r], label=k if i else None)
        if v >= 10:
            ax.text(left + v / 2, i, str(v), ha="center", va="center", fontsize=10,
                    bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
        left += v
ax.set_yticks([0, 1]); ax.set_yticklabels(["first build", "with outbox"]); ax.set_xlabel("claims")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=5, fontsize=9, edgecolor=S.PAL["light"])
save(fig, 15, data="04-code/ch19/output/reconcile_caldwell.txt")
