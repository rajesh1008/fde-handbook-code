"""Figure 28.8: what each layer adds to one referral's latency."""
import re
from _common import S, save, text
t = text("replay")
rows = re.findall(r"^  ((?:input|output|action|budget), [a-z-]+) \((\d+)\)\s+\$([\d.]+)\s+(\d+) ms", t, re.M)
draft_ms = int(re.search(r"the draft itself \(Ch20\)\s+\$[\d.]+\s+(\d+) ms", t).group(1))
fig, ax = S.figure(height=4.0)
labs = [f"{k} ({n})" for k, n, _, _ in rows] + ["the draft itself"]
ms = [int(m) for *_, m in rows] + [draft_ms]
for i, (lab, v) in enumerate(zip(labs, ms)):
    r = "cost" if i == len(ms) - 1 else ("model" if "model" in lab else "system")
    ax.barh(i, v, color=S.ROLE[r], hatch=S.HATCH[r], edgecolor="white", height=0.6)
    ax.text(v * 1.15, i, f"{v:,} ms", va="center", fontsize=9, color=S.PAL["ink"])
ax.set_xscale("log"); ax.set_xlim(0.5, 60000)
ax.set_yticks(range(len(labs)), labs, fontsize=9); ax.set_xlabel("milliseconds per referral (log scale)")
ax.invert_yaxis(); ax.spines[["top", "right"]].set_visible(False)
save(fig, 8, data="04-code/ch28/output/replay.txt")
