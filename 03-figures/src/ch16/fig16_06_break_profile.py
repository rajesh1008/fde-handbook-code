"""Figure 16.6: remove one piece of discovered structure from the v2 profile and the classifier finds it."""
import re
from _common import S, save, text
fig, ax = S.figure(height=3.9)
rows = [(m.group(1).strip(), float(m.group(2))) for m in re.finditer(r"^(.+?)\s+auc (\d\.\d+)", text("tryit_a"), re.M)]
for x, (lab, auc) in enumerate(rows):
    role = "evidence" if auc < 0.6 else "cost"
    ax.bar(x, auc, color=S.TINT[role], edgecolor=S.ROLE[role], hatch=S.HATCH[role], lw=S.LW["data"], width=0.55)
    ax.text(x, auc + 0.02, f"{auc:.2f}", ha="center", fontsize=10)
for v, t in ((0.60, "warn 0.60"), (0.75, "fail 0.75")):
    ax.axhline(v, color=S.PAL["slate"], lw=S.LW["data"], ls="--"); ax.text(2.42, v + 0.015, t, ha="right", fontsize=9)
ax.axhline(0.5, color=S.PAL["grey"], lw=S.LW["data"]); ax.text(-0.42, 0.515, "chance", fontsize=9, color=S.PAL["ink"])
ax.set_xticks(range(len(rows))); ax.set_xticklabels(["v2 as built", "v2 without\nfaded scans", "v2 with first\nnotices only"])
ax.set_ylim(0, 1.0); ax.set_ylabel("two-sample classifier AUC")
save(fig, 6, data="04-code/ch16/output/tryit_a.txt")
