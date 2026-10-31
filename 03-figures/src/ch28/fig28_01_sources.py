"""Figure 28.1: where Greystone's 60 rules came from."""
import re
from _common import S, save, text
t = text("elicit")
src = dict((k, int(v)) for k, v in re.findall(r"([a-z]+) (\d+)", re.search(r"by source:\s+(.*)", t).group(1)))
names = {"engineering": "engineering limits", "payer": "payer tables", "boundary": "signed boundary (Ch25)",
         "session": "said in a session", "observed": "seen at the desk", "regulation": "regulation",
         "redteam": "red team", "signed": "signed scoping ruling"}
role = {"engineering": "system", "payer": "data", "boundary": "approval", "session": "model", "observed": "model",
        "regulation": "evidence", "redteam": "blocker", "signed": "approval"}
items = sorted(src.items(), key=lambda x: x[1])
fig, ax = S.figure(height=4.0)
for i, (k, n) in enumerate(items):
    ax.barh(i, n, color=S.ROLE[role[k]], hatch=S.HATCH[role[k]], edgecolor="white", height=0.6)
    ax.text(n + 0.3, i, str(n), va="center", fontsize=10, color=S.PAL["ink"])
ax.set_yticks(range(len(items)), [names[k] for k, _ in items], fontsize=9)
ax.set_xlabel("rules (of 60)"); ax.set_xlim(0, max(src.values()) + 3)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 1, data="04-code/ch28/output/elicit.txt")
