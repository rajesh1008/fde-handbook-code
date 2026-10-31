"""Figure 26.12: the oversight profile on the checked half of gold-set-300, baseline p6 and candidate p7."""
from _common import S, save, js
d = js("oversight")
fig, ax = S.figure(height=3.9)
for k, lab, r, m in (("p6", "baseline p6", "blocker", "o"), ("p7", "candidate p7", "system", "s")):
    xs = [c[1] * 100 for c in d[k]["curve"]]; ys = [c[2] * 100 for c in d[k]["curve"]]
    ax.plot(xs, ys, color=S.ROLE[r], marker=m, ms=4, lw=1.5, label=lab)
for y, lab in ((95, "95%: D-07"), (98, "98%: the promise")):
    ax.axhline(y, color=S.PAL["grey"], ls="--", lw=1)
    ax.text(101, y, lab, va="center", fontsize=9)
ax.set_xlim(0, 125); ax.set_ylim(60, 100)
ax.set_xlabel("share of fields sent without review (%)"); ax.set_ylabel("accuracy of those fields (%)")
ax.legend(loc="lower left", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 12, data="04-code/ch26/output/oversight.json")
