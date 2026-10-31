"""Figure 33.3: the register on days 82, 132 and 153; design changes move components into full scope."""
import re
from _common import S, save, text
t = text("classify")
rows = re.findall(r"day +(\d+): (\d+) components +(.*?)  plan items (\d+)", t)
keys = [("full scope", "approval", "full scope"), ("registered, not validated", "evidence", "registered, not validated"),
        ("registered as a tool", "data", "tool"), ("not a model", "system", "not a model")]
fig, ax = S.figure(height=4.0)
for i, (day, n, rest, items) in enumerate(rows):
    left = 0
    for k, role, lab in keys:
        m = re.search(re.escape(k) + r" (\d+)", rest); v = int(m.group(1)) if m else 0
        if v:
            ax.barh(i, v, left=left, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white", height=0.6,
                    label=lab if i == 2 else None)
            if role != "system" or True:
                ax.text(left + v / 2, i, str(v), ha="center", va="center", fontsize=10,
                        color=S.PAL["ink"], bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
            left += v
    ax.text(left + 0.3, i, f"{items} plan items", va="center", fontsize=9.5)
ax.set_yticks(range(len(rows)), [f"day {d}" for d, *_ in rows]); ax.invert_yaxis()
ax.set_xlim(0, 24); ax.set_xlabel("components")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), fontsize=9, ncol=4, handlelength=1.2, columnspacing=0.8); ax.spines[["top", "right"]].set_visible(False)
save(fig, 3, data="04-code/ch33/output/classify.txt")
