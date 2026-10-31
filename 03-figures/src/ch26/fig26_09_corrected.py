"""Figure 26.9: what each judge reports, before and after correction, against Anne's adjusters."""
from _common import S, save, js
d = js("judge_validation")
fig, ax = S.figure(height=3.8)
rows = [("v1 raw", d["judge_v1"]["raw"], None, "model"), ("v1 corrected", d["judge_v1"]["corr"],
        (d["judge_v1"]["lo"], d["judge_v1"]["hi"]), "evidence"), ("v2 raw", d["judge_v2"]["raw"], None, "model"),
        ("v2 corrected", d["judge_v2"]["corr"], (d["judge_v2"]["lo"], d["judge_v2"]["hi"]), "evidence")]
for i, (lab, v, ci, r) in enumerate(rows):
    y = 3 - i
    ax.scatter([v * 100], [y], color=S.ROLE[r], s=60, zorder=3)
    if ci:
        ax.plot([ci[0] * 100, ci[1] * 100], [y, y], color=S.ROLE[r], lw=2.5)
    ax.text(v * 100, y + 0.25, f"{v:.1%}", ha="center", fontsize=10)
ax.axvline(d["anne"] * 100, color=S.ROLE["approval"], lw=2)
ax.text(d["anne"] * 100 + 0.5, -0.6, "Anne's adjusters", color=S.PAL["ink"], fontsize=10)
ax.set_yticks(range(4), [r[0] for r in rows[::-1]])
ax.set_xlim(55, 90); ax.set_ylim(-0.9, 3.6); ax.set_xlabel("pass rate on the held-out split (%)")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 9, data="04-code/ch26/output/judge_validation.json")
