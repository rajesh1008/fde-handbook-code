"""Figure 40.7: gateway trace tokens minus the tokens of the rebuilt input (commit text plus document)."""
from _common import S, save, text
import ast
part = text("rerun").split("TOKEN GAP")[1].split("RERUN")[0]
pts = []
for l in part.splitlines():
    if l.strip().startswith("day"):
        d = int(l.split(":")[0].split()[1]); g = ast.literal_eval(l.split("gaps ")[1])
        pts += [(d, x) for x in g]
assert (166, 35) in pts and (165, 0) in pts
fig, ax = S.figure(height=3.7)
xs0 = [d for d, g in pts if g == 0]; xs1 = [d for d, g in pts if g > 0]
ax.plot(xs0, [0] * len(xs0), "o", color=S.ROLE["system"], ms=7, label="gap 0: rebuilt input matches")
ax.plot(xs1, [35] * len(xs1), "s", color=S.ROLE["blocker"], ms=7, label="gap 35: text in force was longer")
ax.set_ylim(-8, 48); ax.set_xlim(157, 180); ax.set_xlabel("engagement day"); ax.set_ylabel("token gap per call")
ax.legend(fontsize=9.5, loc="center left"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 7, data="04-code/ch40/output/rerun.txt")
