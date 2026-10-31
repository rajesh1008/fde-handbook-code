"""Figure 19.17: one day of carrier status messages, from transaction sets to reconciled legs."""
import re
from _common import S, save, text, dct
t = text("pennant_edi")
env, unk, parsed = map(int, re.search(r"envelope errors (\d+), unknown codes (\d+), parsed (\d+)", t).groups())
r = dct(re.search(r"02:00 export: (\{.*?\})", t).group(1))
fig, ax = S.figure(height=4.0)
lab = ["envelope\nerrors", "unknown\ncodes", "matched", "status\ndiffers", "unknown\nto TMS"]
v = [env, unk, r["matched"], r["mismatched"], r["missing"]]
roles = ["blocker", "blocker", "approval", "data", "cost"]
ax.bar(range(5), v, color=[S.TINT[x] for x in roles], edgecolor=[S.ROLE[x] for x in roles],
       hatch=[S.HATCH[x] for x in roles])
for i, n in enumerate(v):
    ax.text(i, n * 1.15 + 0.3, str(n), ha="center", fontsize=10)
ax.set_yscale("symlog", linthresh=10); ax.set_ylim(0, 800); ax.set_xticks(range(5)); ax.set_xticklabels(lab)
ax.set_ylabel("count (log scale)")
save(fig, 17, data="04-code/ch19/output/pennant_edi.txt")
