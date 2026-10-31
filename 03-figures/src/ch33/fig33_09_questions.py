"""Figure 33.9: the validator's 14 questions under the one-model and the component framing."""
import re
from _common import S, save, text
t = text("validator")
rows = re.findall(r"^(one-model|component) framing \(day (\d+)\): +evidence (\d+) +translation (\d+) +boundary (\d+)", t, re.M)
kinds = [("evidence", "approval"), ("translation", "evidence"), ("boundary", "blocker")]
fig, ax = S.figure(height=3.8)
for i, (name, day, *v) in enumerate(rows):
    left = 0
    for (k, role), n in zip(kinds, map(int, v)):
        if n:
            ax.barh(i, n, left=left, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white", height=0.55,
                    label=k if i == 1 else None)
            ax.text(left + n / 2, i, str(n), ha="center", va="center", fontsize=10,
                    bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
            left += n
ax.set_yticks(range(len(rows)), [f"{n}, day {d}" for n, d, *_ in rows]); ax.invert_yaxis()
ax.set_xlim(0, 14.5); ax.set_xlabel("questions in the day-74 request")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.55), ncol=3, fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 9, data="04-code/ch33/output/validator.txt")
