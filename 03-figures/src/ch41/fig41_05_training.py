"""Figure 41.5: share of competence-check tasks done alone, by session, operators against engineers."""
from _common import S, save, text, nums
fig, ax = S.figure(height=4.0)
rows = [l for l in text("training").splitlines() if " day " in l]
for cohort, r, m in (("operators", "approval", "o"), ("engineers", "model", "s")):
    pts = [(nums(l.split("day")[1])[0], float(l.split("=")[1].split()[0])) for l in rows if l.startswith(cohort)]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], marker=m, color=S.ROLE[r], lw=S.LW["control"], label=cohort)
    ax.text(pts[-1][0] + 0.4, pts[-1][1], f"{pts[-1][1]:.2f}", va="center", fontsize=9)
ax.set_xticks([165, 170, 175, 180]); ax.set_ylim(0, 1.08); ax.set_xlim(164, 183); ax.set_xlabel("day"); ax.set_ylabel("share done alone")
ax.legend(loc="upper left", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch41/output/training.txt")
