"""Figure 30.9: Anne's-set accuracy by number of clerk labels, against c06-p4 (Listing 30.6)."""
from _common import S, save, text, nums
rows = [nums(l) for l in text("labels").splitlines() if l.strip()[:1].isdigit()]
ref = nums([l for l in text("labels").splitlines() if l.startswith("c06-p4 reference")][0])[1]
x = [r[0] for r in rows]
fig, ax = S.figure(height=3.9)
ax.plot(x, [r[2] for r in rows], color=S.ROLE["system"], lw=S.LW["emphasis"], marker="o")
ax.plot(x, [r[4] for r in rows], color=S.ROLE["approval"], lw=S.LW["control"], ls="--", marker="s")
ax.axhline(ref, color=S.ROLE["model"], lw=S.LW["control"])
ax.set_xscale("log"); ax.set_xticks(x, [f"{int(v):,}" for v in x], fontsize=9); ax.minorticks_off()
ax.set_ylim(45, 100); ax.set_xlabel("clerk-labeled training documents"); ax.set_ylabel("Anne's set typed right (%)")
S.label(ax, 110, ref + 1.2, f"c06-p4 {ref:.1f}%", color=S.ROLE["model"], fs=9)
S.label(ax, 2300, rows[-1][2] - 6, "fine-tuned", color=S.ROLE["system"], fs=9)
S.label(ax, 120, 50, "fine-tuned + guard (dashed)", color=S.PAL["ink"], fs=9)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 9, data="04-code/ch30/output/labels.txt")
