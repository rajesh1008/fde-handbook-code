"""Figure 30.5: cost per thousand documents and latency, prompted vs fine-tuned (Listing 30.3)."""
from _common import S, save, text, nums
t = text("cost").splitlines()
import re
fr, ft = [float(x) for x in re.findall(r"\$([0-9.]+)", t[0])]
frc = float(re.findall(r"\$([0-9.]+)", t[1])[0])
lat = [nums(l.split("p50")[1])[0::2] for l in t if l.startswith("latency")]
fig, (a1, a2) = S.figure(height=3.9, ncols=2, gridspec_kw=dict(width_ratios=[1.25, 1]))
v = [1000 * fr, 1000 * frc, 1000 * ft]
a1.bar(range(3), v, color=[S.ROLE["model"], S.TINT["model"], S.ROLE["system"]], edgecolor=S.ROLE["model"], width=0.6)
for i, y in enumerate(v):
    S.label(a1, i, y + 0.3, f"${y:.2f}", ha="center", fs=9)
a1.set_xticks(range(3), ["prompted", "prompted,\ncached", "fine-\ntuned"], fontsize=9)
a1.set_ylabel("cost per 1,000 documents ($)"); a1.set_ylim(0, 13)
for i, (p50, p95) in enumerate(lat):
    c = S.ROLE["model"] if i == 0 else S.ROLE["system"]
    a2.bar(i - 0.18, p50, 0.34, color=c); a2.bar(i + 0.18, p95, 0.34, color=S.TINT["model" if i == 0 else "system"], edgecolor=c)
    S.label(a2, i - 0.18, p50 + 0.15, f"{p50:.2f}", ha="center", fs=9); S.label(a2, i + 0.18, p95 + 0.15, f"{p95:.2f}", ha="center", fs=9)
a2.set_xticks([0, 1], ["prompted", "fine-\ntuned"], fontsize=9); a2.set_ylabel("seconds (p50, p95)"); a2.set_ylim(0, 7.8)
for a in (a1, a2):
    a.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch30/output/cost.txt")
