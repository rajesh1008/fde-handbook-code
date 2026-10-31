"""Figure 32.6: what the 41 answers claim: measured, configured, documented or assumed."""
import re
from _common import S, save, text
c = dict(re.findall(r"(measured|configured|documented|assumed) (\d+)", text("triage").split("claims:")[1].splitlines()[0]))
ks = ["measured", "configured", "documented", "assumed"]; roles = ["approval", "system", "evidence", "blocker"]
fig, ax = S.figure(height=3.8)
for i, (k, r) in enumerate(zip(ks, roles)):
    v = int(c[k]); ax.bar(i, v, color=S.TINT[r], edgecolor=S.ROLE[r], hatch=S.HATCH[r], lw=1.5)
    ax.text(i, v + 0.5, str(v), ha="center", fontsize=10)
ax.set_xticks(range(4)); ax.set_xticklabels(ks); ax.set_ylabel("answers"); ax.set_ylim(0, 28)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 6, data="04-code/ch32/output/triage.txt")
