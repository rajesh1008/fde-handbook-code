"""Figure 19.14: why 13 of 152 writes went to a person after the fix, by reason."""
import re
from _common import S, save, text, dct
held = dct(re.search(r"held, by reason  : (\{.*\})", text("writeback_fixed")).group(1).replace(" ", "_"))
m = re.findall(r"'([^']+)': (\d+)", re.search(r"held, by reason  : (\{.*\})", text("writeback_fixed")).group(1))
fig, ax = S.figure(height=3.8)
names = {"preflight V-118": "preflight: V-118\nno cause code", "rejected V-127": "screen 2: V-127\nshell voided",
         "readback differs": "read-back:\nname truncated"}
v = [int(n) for _, n in m]
roles = ["evidence", "blocker", "data"]
ax.barh(range(len(m)), v, color=[S.TINT[r] for r in roles], edgecolor=[S.ROLE[r] for r in roles],
        hatch=[S.HATCH[r] for r in roles])
for i, n in enumerate(v):
    ax.text(n + 0.2, i, str(n), va="center", fontsize=10)
ax.set_yticks(range(len(m))); ax.set_yticklabels([names[k] for k, _ in m]); ax.invert_yaxis()
ax.set_xlabel("first notices held"); ax.set_xlim(0, 13)
save(fig, 14, data="04-code/ch19/output/writeback_fixed.txt")
