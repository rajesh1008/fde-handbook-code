"""Figure 24.13: answers still shown after the rollback decision, flag in the surface only versus in the brain (rollback.txt)."""
import re
from _common import S, save, text
t = text("rollback")
cum = {k: [(float(m), int(n)) for m, n in re.findall(r"([\d.]+)m=(\d+)", v)] for k, v in re.findall(r"^cumulative answers shown, ([a-z -]+): (.+)$", t, re.M)}
fig, ax = S.figure(height=4.0)
sty = {"client-side": (S.ROLE["blocker"], "surface flag only"), "in brain": (S.ROLE["approval"], "flag enforced in brain")}
for k, pts in cum.items():
    c, lab = sty[k]
    ax.step([p[0] for p in pts], [p[1] for p in pts], where="post", color=c, lw=S.LW["emphasis"])
    ax.text(pts[-1][0] * 0.62, pts[-1][1] + 2.5, f"{lab}: {pts[-1][1]}", fontsize=10, color=S.PAL["ink"], ha="center")
ax.set_xscale("log"); ax.set_xticks([0.5, 1, 5, 30, 60, 180], ["0.5", "1", "5", "30", "60", "180"])
ax.set_xlim(0.4, 260); ax.set_ylim(0, 62)
ax.set_xlabel("minutes after the mode change (log scale)"); ax.set_ylabel("answers still shown, cumulative")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 13, data="04-code/ch24/output/rollback.txt")
