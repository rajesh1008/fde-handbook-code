"""Figure 41.4: reading paths through the engagement reference; coral marks the three gaps in v1, closed in v2."""
from _common import S, save, text
import sys; sys.path.insert(0, str(__import__("_common").R / "04-code/ch41"))
import world as W
fig, ax = S.figure(height=4.6)
st = list(W.NEEDS); secs = list(W.SECTIONS)
for yi, s in enumerate(st):
    for x in secs:
        if x in W.PATHS_V1[s]:
            ax.scatter(x, yi, s=90, color=S.ROLE["system"], marker="s")
        elif x in W.PATHS_V2[s]:
            ax.scatter(x, yi, s=110, color=S.ROLE["blocker"], marker="D")
ax.set_yticks(range(len(st))); ax.set_yticklabels(st); ax.invert_yaxis()
ax.set_xticks(secs); ax.set_xlabel("section of the engagement reference")
ax.scatter([], [], color=S.ROLE["system"], marker="s", label="on the v1 path")
ax.scatter([], [], color=S.ROLE["blocker"], marker="D", label="missing in v1, added in v2")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2, fontsize=9); ax.spines[["top", "right"]].set_visible(False)
assert "paths with gaps: 3 of 7" in text("reference_v1")
save(fig, 4, data="04-code/ch41/world.py PATHS_V1, PATHS_V2; output/reference_v1.txt, reference_v2.txt")
