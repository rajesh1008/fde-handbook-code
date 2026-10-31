"""Figure 19.7: documents stored from 103 mailbox messages (88 real documents) under three dedupe rules."""
import re
from _common import S, save, text
rows = re.findall(r"^(.+?)\s+documents stored\s+(\d+)", text("mail_queue"), re.M)
fig, ax = S.figure(height=3.8)
lab = ["none", "Message-ID", "Message-ID +\nattachment hash"]
v = [int(n) for _, n in rows]
ax.bar(range(3), v, color=[S.TINT["blocker"], S.TINT["data"], S.TINT["approval"]],
       edgecolor=[S.ROLE["blocker"], S.ROLE["data"], S.ROLE["approval"]], hatch="..")
ax.axhline(88, color=S.PAL["ink"], lw=S.LW["control"], ls="--")
ax.text(2.45, 89.5, "88 real", ha="right", fontsize=9.5)
for i, n in enumerate(v):
    ax.text(i, n + 1, str(n), ha="center", fontsize=10)
ax.set_xticks(range(3)); ax.set_xticklabels(lab); ax.set_ylim(70, 110); ax.set_ylabel("documents stored")
save(fig, 5, data="04-code/ch19/output/mail_queue.txt")
