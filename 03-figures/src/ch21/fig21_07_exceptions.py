"""Figure 21.7: downstream exceptions by cause on the same 2,000 documents, without and with the scorer."""
from _common import S, save, text, dct
t = text("scorer").splitlines()
wo = dct([l for l in t if l.startswith("downstream exceptions without")][0])
wi = dct([l for l in t if l.startswith("downstream exceptions with the")][0])
order = [("clean", "clean document", S.PAL["grey"]), ("marginal", "marginal page", S.PAL["slate"]),
         ("misread", "misread, invisible", S.ROLE["cost"]), ("illegible", "illegible", S.ROLE["blocker"]),
         ("missing", "missing field", S.ROLE["data"]), ("inconsistent", "lines do not sum", S.ROLE["model"]),
         ("bad_container", "bad container no.", S.ROLE["system"])]
fig, ax = S.figure(height=3.9)
for y, d in ((1, wo), (0, wi)):
    left = 0
    for k, lab, c in order:
        v = d.get(k, 0)
        if v:
            ax.barh(y, v, left=left, color=c, height=0.5, label=lab if y == 1 else None, edgecolor="white")
            left += v
    ax.text(left + 4, y, f"{left}", va="center", fontsize=11, color=S.PAL["ink"], weight="bold")
ax.set_yticks([1, 0], ["without\nscorer", "with\nscorer"]); ax.set_xlim(0, 430)
ax.set_xlabel("downstream exceptions")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, fontsize=9.5, frameon=False)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 7, data="04-code/ch21/output/scorer.txt")
