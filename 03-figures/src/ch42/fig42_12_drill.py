"""Figure 42.12: time to detect, acknowledge and mitigate, the night of day 38 (v0) and the day-70 drill (v2)."""
import re
from _common import S, save, text, plt
val = {m: [int(v) for v in re.findall(r"(\d+) min", [l for l in text(f"drill_{m}").splitlines() if l.startswith("time to detect")][0])] for m in ("v0", "v2")}
fig, ax = S.figure(height=4.0)
lab = ["detect", "acknowledge", "mitigate"]
for i, (m, c, n) in enumerate((("v0", "blocker", "day 38, as handed over"), ("v2", "approval", "day 70 drill, runbook v2"))):
    ax.barh([j + 0.2 - 0.4 * i for j in range(3)], val[m], 0.38, color=S.ROLE[c], label=n)
    for j, v in enumerate(val[m]):
        ax.text(v + 0.8, j + 0.2 - 0.4 * i, f"{v}", va="center", fontsize=9)
ax.axvline(30, color=S.PAL["ink"], ls="--", lw=S.LW["control"]); ax.text(30.5, -0.55, "Live Stable line, 30", fontsize=9)
ax.set_yticks(range(3)); ax.set_yticklabels(lab); ax.invert_yaxis(); ax.set_xlabel("minutes"); ax.legend(fontsize=9, loc="center right")
save(fig, 12, kind="plot", data="04-code/ch42/output/drill_v0.txt, drill_v2.txt")
