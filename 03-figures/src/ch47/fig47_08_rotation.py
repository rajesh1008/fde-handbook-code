"""Figure 47.8: anchor changes as customers saw them: overlap and notice before and after the anchor rule."""
from _common import S, save
import sys
sys.path.insert(0, str(S.ROOT / "04-code/ch47"))
from world import CHANGES_BEFORE, CHANGES_AFTER  # noqa: E402
fig, ax = S.figure(height=4.0)
from matplotlib.patches import Rectangle
ax.add_patch(Rectangle((10, 30), 10, 25, fc=S.TINT["approval"], ec="none"))
ax.text(10.4, 51, "rule: 10 days overlap,\n30 days notice", fontsize=9, va="top")
for ch, c, m, lab in ((CHANGES_BEFORE, S.ROLE["blocker"], "X", "months 13 to 15"),
                      (CHANGES_AFTER, S.ROLE["system"], "o", "months 16 to 18")):
    ax.plot([x[4] for x in ch], [x[5] for x in ch], marker=m, ls="none", color=c, ms=8, label=lab)
for cust, mth, o, n, ov, no in CHANGES_BEFORE:
    if cust == "N08":
        ax.text(ov + 0.4, no + 1.2, f"N08 m{mth}", fontsize=9)
ax.set_xlim(-1, 20); ax.set_ylim(-3, 55); ax.set_xlabel("overlap working days"); ax.set_ylabel("notice days")
ax.legend(loc="lower right", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 8, data="04-code/ch47/output/rotation.txt; world.py CHANGES_BEFORE, CHANGES_AFTER")
