"""Figure 32.15: open findings from day 103, closed only with retest evidence; plan to day 128."""
import re
from _common import S, save, text
t = text("remediation")
act = [(int(a), int(b)) for a, b in re.findall(r"d(\d+) (\d+)", t.split("burn-down:")[1].splitlines()[0])]
plan = [(int(a), int(b)) for a, b in re.findall(r"d(\d+) (\d+)", t.split("date:")[1].splitlines()[0])]
fig, ax = S.figure(height=3.9)
ax.step([d for d, _ in act], [n for _, n in act], where="post", color=S.ROLE["blocker"], lw=S.LW["emphasis"], label="open, actual")
ax.step([d for d, _ in plan], [n for _, n in plan], where="post", color=S.ROLE["evidence"], lw=S.LW["control"], ls="--", label="open, if retests land on date")
ax.axvline(113, color=S.PAL["grey"], lw=0.75, ls=":"); ax.text(113.4, 11, "sandbox read\nsigned, day 113", fontsize=9)
ax.set_xlabel("engagement day"); ax.set_ylabel("open findings"); ax.set_ylim(0, 13); ax.set_xlim(102, 130)
ax.legend(fontsize=9, loc="lower left"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 15, data="04-code/ch32/output/remediation.txt")
