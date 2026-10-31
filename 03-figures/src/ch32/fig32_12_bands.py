"""Figure 32.12: threats by risk band before and with controls."""
import re
from _common import S, save, text
def dct(line): return {k: int(v) for k, v in re.findall(r"(high|medium|low)\D+?(\d+)", line)}
t = text("threat_model")
inh = dct([l for l in t.splitlines() if l.startswith("inherent")][0]); res = dct([l for l in t.splitlines() if l.startswith("with controls")][0])
ks = ["high", "medium", "low"]
import numpy as np
x = np.arange(3); fig, ax = S.figure(height=3.8)
ax.bar(x - 0.2, [inh[k] for k in ks], 0.4, color=S.TINT["blocker"], edgecolor=S.ROLE["blocker"], hatch=S.HATCH["blocker"], label="inherent")
ax.bar(x + 0.2, [res[k] for k in ks], 0.4, color=S.TINT["approval"], edgecolor=S.ROLE["approval"], label="with controls, day 103")
for i, k in enumerate(ks):
    ax.text(i - 0.2, inh[k] + 0.3, str(inh[k]), ha="center", fontsize=10); ax.text(i + 0.2, res[k] + 0.3, str(res[k]), ha="center", fontsize=10)
ax.text(0.2, res["high"] + 1.4, "all four\nare findings", ha="center", fontsize=9)
ax.set_xticks(x); ax.set_xticklabels(ks); ax.set_ylabel("threats"); ax.set_ylim(0, 18); ax.legend(fontsize=9, loc="upper right")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 12, data="04-code/ch32/output/threat_model.txt")
