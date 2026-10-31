"""Figure 19.3: open facts in the surface inventory, by customer and kind of fact."""
import re
from _common import S, save, text
rows = re.findall(r"^(caldwell|greystone|pennant)\S* +\S.*?\d\.\d\d   (.*)$", text("inventory"), re.M)
facts = ["owner", "sample", "failure_contact", "change_notice"]
cust = ["caldwell", "greystone", "pennant"]
cnt = {c: [sum(f in g.split(",") for cc, g in rows if cc == c) for f in facts] for c in cust}
fig, ax = S.figure(height=4.0)
roles = ["blocker", "data", "evidence", "cost"]
left = [0] * 3
for j, f in enumerate(facts):
    v = [cnt[c][j] for c in cust]
    ax.barh(range(3), v, left=left, color=S.TINT[roles[j]], edgecolor=S.ROLE[roles[j]], hatch=S.HATCH[roles[j]],
            label=f.replace("_", " "))
    left = [a + b for a, b in zip(left, v)]
for i, t in enumerate(left):
    ax.text(t + 0.2, i, str(t), va="center", fontsize=10)
ax.set_yticks(range(3)); ax.set_yticklabels([c.title() for c in cust])
ax.set_xlabel("open facts across surfaces"); ax.invert_yaxis()
ax.legend(loc="lower right", fontsize=9, edgecolor=S.PAL["light"])
save(fig, 3, data="04-code/ch19/output/inventory.txt")
