"""Figure 24.7: win share under 2,000 weight draws, and the winner per user group (options.txt)."""
import re
from _common import S, save, text
t = text("options")
wins = re.findall(r"^  ([ABCD]) wins\s+\d+ \(([\d.]+)%\)", t, re.M)
groups = re.findall(r"^  (adjusters|supervisors|intake clerks)\s+(.+?)\s+winner (\w)$", t, re.M)
fig, (a1, a2) = S.figure(height=4.0, ncols=2)
col = {"A": S.PAL["amber"], "B": S.PAL["slate"], "C": S.PAL["teal"], "D": S.PAL["grey"]}
for k, v in wins:
    a1.bar(k, float(v), color=col[k]); a1.text(k, float(v) + 1.5, f"{float(v):.1f}%", ha="center", fontsize=10)
a1.set_ylim(0, 90); a1.set_ylabel("share of weight draws won"); a1.set_title("2,000 weight draws", fontsize=10, loc="left")
for i, (g, sc, w) in enumerate(groups):
    for k, v in re.findall(r"([ABCD]) ([\d.]+)", sc):
        a2.plot(float(v), i, "o", color=col[k], ms=7)
        if k in "AC":
            a2.text(float(v), i + 0.22, k, ha="center", fontsize=10, color=S.PAL["ink"], weight="bold" if k == w else "normal")
a2.set_yticks(range(len(groups)), [g for g, *_ in groups]); a2.set_ylim(-0.6, len(groups) - 0.2)
a2.set_xlim(55, 88); a2.set_xlabel("total, 0-100"); a2.set_title("per user group", fontsize=10, loc="left")
for a in (a1, a2):
    a.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
save(fig, 7, data="04-code/ch24/output/options.txt")
