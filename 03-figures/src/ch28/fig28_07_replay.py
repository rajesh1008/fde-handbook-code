"""Figure 28.7: what the suite did with the sandbox week."""
import re
from _common import S, save, text
t = text("replay").split("suite v2")[0]
rows = re.findall(r"^  ((?:queued|routed|blocked)[a-z ,]*?)\s{2,}(\d+)$", t, re.M)
role = lambda k: "approval" if k == "queued" else "data" if k.startswith("queued") else "blocker" if k.startswith("blocked") else "evidence"  # noqa: E731
rows = sorted(((k, int(v)) for k, v in rows), key=lambda x: x[1])
fig, ax = S.figure(height=4.0)
for i, (k, v) in enumerate(rows):
    ax.barh(i, v, color=S.ROLE[role(k)], hatch=S.HATCH[role(k)], edgecolor="white", height=0.6)
    ax.text(v + 1.5, i, str(v), va="center", fontsize=10, color=S.PAL["ink"])
ax.set_yticks(range(len(rows)), [k for k, _ in rows], fontsize=9)
ax.set_xlabel("referrals (of 200)"); ax.set_xlim(0, 130); ax.spines[["top", "right"]].set_visible(False)
save(fig, 7, data="04-code/ch28/output/replay.txt")
