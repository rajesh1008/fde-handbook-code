"""Figure 47.5: field reports by sales votes and by evidence score; the two shipped features sit top left."""
from _common import S, save
import sys
sys.path.insert(0, str(S.ROOT / "04-code/ch47"))
import _paths  # noqa: F401,E402
from fieldkit.playbooks import FieldReport, evidence_score  # noqa: E402
from world import REPORTS  # noqa: E402
fig, ax = S.figure(height=4.2)
seen = {}
for rid, t, o, e, h, v, a, art, fm in REPORTS:
    r = FieldReport(rid, t, o, list(e), [h] * len(e), v, a, art, fm)
    s = evidence_score(r)
    shipped = rid in ("FR-001", "FR-002")
    ax.plot(v, s, marker="s" if shipped else ("o" if s else "X"), ms=9 if shipped else 7,
            color=S.ROLE["approval"] if shipped else (S.ROLE["evidence"] if s else S.ROLE["blocker"]), ls="none")
    k = (v, round(s / 40)); dy = -38 * seen.get(k, 0); seen[k] = seen.get(k, 0) + 1
    ax.text(v + 0.2, s + 14 + dy, rid, fontsize=9)
ax.set_xlabel("votes from sales and account teams"); ax.set_ylabel("evidence score (hours)")
ax.set_xlim(-0.5, 11); ax.set_ylim(-40, 800)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([], [], marker="s", ls="none", color=S.ROLE["approval"], label="shipped"),
                   Line2D([], [], marker="o", ls="none", color=S.ROLE["evidence"], label="has working code"),
                   Line2D([], [], marker="X", ls="none", color=S.ROLE["blocker"], label="no artifact")],
          loc="upper right", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch47/output/loop_rank.txt; world.py REPORTS")
