"""Figure 24.9: one turn with the fan-out run in sequence (injected failure) and in parallel (fanout.txt, turn 1)."""
import re
from _common import S, save, text
t = text("fanout")
runs = dict(re.findall(r"^  (sequential|parallel): (.+)$", t, re.M))
fig, axes = S.figure(height=4.6, nrows=2, sharex=True)
for ax, k in zip(axes, ("sequential", "parallel")):
    calls = re.findall(r"([a-z-]+) (\d+)-(\d+)", runs[k]); tot = int(re.search(r"total (\d+)", runs[k]).group(1))
    for i, (n, a, b) in enumerate(calls):
        a, b = int(a), int(b)
        ax.barh(len(calls) - 1 - i, b - a, left=a, color=S.ROLE["blocker"] if n == "claims-core" else S.ROLE["system"], height=0.6)
    ax.set_yticks(range(len(calls)), [c[0] for c in calls][::-1], fontsize=10)
    fan = max(int(c[2]) for c in calls)
    ax.axvline(fan, color=S.PAL["ink"], lw=0.75, ls="--")
    ax.set_title(f"{k}: fan-out {fan:,} ms, whole turn {tot:,} ms", fontsize=10, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
axes[1].set_xlabel("ms from the start of the fan-out"); axes[1].set_xlim(0, 6500)
fig.tight_layout()
save(fig, 9, data="04-code/ch24/output/fanout.txt")
