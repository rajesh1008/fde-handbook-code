"""Figure 19.13: the same 152 writes, accepted in UAT, then run against the production rule table."""
import re
from _common import S, save, text, dct
t = text("writeback_failure")
acc = [int(x) for x in re.findall(r"accepted (\d+)", t)]
st = [dct(s) for s in re.findall(r"by status (\{.*?\})", t)]
dup = [int(x) for x in re.findall(r"duplicate claims (\d+)", t)]
fig, ax = S.figure(height=4.0)
lab = ["accepted", "orphan shells", "duplicates"]
for j, (env, r) in enumerate([("UAT", "approval"), ("pre-production", "blocker")]):
    v = [acc[j], st[j].get("SHELL", 0), dup[j]]
    xs = [i + (j - 0.5) * 0.38 for i in range(3)]
    ax.bar(xs, v, 0.36, color=S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH["evidence"] if j else "", label=env)
    for x, n in zip(xs, v):
        ax.text(x, n + 2, str(n), ha="center", fontsize=10)
ax.set_xticks(range(3)); ax.set_xticklabels(lab); ax.set_ylabel("claims"); ax.set_ylim(0, 172)
ax.legend(loc="upper right", fontsize=9.5, edgecolor=S.PAL["light"])
save(fig, 12, data="04-code/ch19/output/writeback_failure.txt")
