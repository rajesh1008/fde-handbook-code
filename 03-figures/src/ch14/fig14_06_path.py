"""Figure 14.6: the critical path from the signed scope (day 19) to the projected pilot (day 140)."""
from _common import S, save, plt
import pipeline as pl, projection as pj

i = pj.Inputs(); p = pj.project(pl.ELECTRONIC)
bars = [("build on synthetic packets", i.scope_day, p["build_done"], "system"),
        ("privacy board submission", i.board_submission_day, p["board"], "approval"),
        ("Architecture Review wait", i.scope_day, i.arch_review_day, "blocker"),
        ("managed-service provider change", i.arch_review_day, p["data"], "blocker"),
        ("evaluation + clinical sign-off", p["data"], p["pilot"], "evidence")]
fig, ax = S.figure(3.9)
for k, (n, a, b, role) in enumerate(bars):
    ax.barh(k, b - a, left=a, height=0.5, color=S.TINT[role], edgecolor=S.ROLE[role], hatch=S.HATCH[role], lw=1.2)
    ax.text(b + 2, k, f"day {b}", va="center", fontsize=9.5)
ax.set_yticks(range(len(bars))); ax.set_yticklabels([b[0] for b in bars], fontsize=9.5); ax.invert_yaxis()
ax.axvline(p["pilot"], color=S.PAL["ink"], lw=S.LW["emphasis"])
ax.text(p["pilot"] - 2, -0.75, f"pilot day {p['pilot']}", ha="right", fontsize=10, weight="bold")
ax.set_xlim(10, 165); ax.set_ylim(4.8, -1.2); ax.set_xlabel("engagement day")
ax.text(12, 4.45, f"critical path: data; build slack {p['slack']} days", fontsize=9.5)
save(fig, 6)
