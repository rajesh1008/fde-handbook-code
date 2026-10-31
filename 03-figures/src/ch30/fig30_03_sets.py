"""Figure 30.3: c06-ft1 and c06-p4 on the test split, Anne's set and the legal-60 slice (Listing 30.1)."""
from _common import S, save, text, nums
rows = [l for l in text("failure_injection").splitlines() if l.startswith(("history test", "Anne's set (", "legal-60 mis"))]
names = ["history test split\n(clerk labels)", "Anne's set\n(adjuster labels)", "legal-60\nmisfile slice"]
vals = []
for l in rows:
    n = nums(l.split(")")[-1] if "(" in l else l)
    vals.append((n[-4], n[-3], n[-2], n[-1]))   # ft count, ft pct, p4 count, p4 pct
fig, ax = S.figure(height=3.9)
for i, (fc, fp, pc, pp) in enumerate(vals):
    ax.bar(i - 0.2, fp, 0.38, color=S.ROLE["system"], hatch=S.HATCH["system"], edgecolor="white")
    ax.bar(i + 0.2, pp, 0.38, color=S.ROLE["model"])
    S.label(ax, i - 0.2, fp + 1.5, f"{fp:.1f}%", ha="center", fs=9)
    S.label(ax, i + 0.2, pp + 1.5, f"{pp:.1f}%", ha="center", fs=9)
ax.set_xticks(range(3), names, fontsize=9); ax.set_ylim(0, 112); ax.set_ylabel("documents typed right (%)")
S.label(ax, -0.45, 104, "c06-ft1, fine-tuned", color=S.ROLE["system"], fs=9)
S.label(ax, 1.15, 104, "c06-p4, prompted frontier", color=S.ROLE["model"], fs=9)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 3, data="04-code/ch30/output/failure_injection.txt")
