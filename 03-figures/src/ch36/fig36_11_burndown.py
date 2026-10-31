"""Figure 36.12: open security findings by engagement day; the red team raises eleven on day 127."""
from _common import S, save, text
line = next(l for l in text("retest").splitlines() if l.startswith("BURNDOWN"))
tok = line.split(": ", 1)[1].split()
pts = [(int(tok[i][1:]), int(tok[i + 1])) for i in range(0, len(tok), 2)]
assert dict(pts)[127] == 12 and dict(pts)[129] == 2
fig, ax = S.figure(height=4.0)
d, n = zip(*pts)
ax.step(d, n, where="post", color=S.ROLE["evidence"], lw=2.5)
ax.annotate("red-team findings raised", xy=(127, 12), xytext=(108, 12.5), fontsize=9.5,
            arrowprops=dict(arrowstyle="-|>", mutation_scale=10, color=S.PAL["ink"], lw=1.5))
ax.annotate("F-13 and F-21 open,\naccepted as residual", xy=(129, 2), xytext=(108, 4.2), fontsize=9.5,
            arrowprops=dict(arrowstyle="-|>", mutation_scale=10, color=S.PAL["ink"], lw=1.5))
ax.set_xlabel("engagement day"); ax.set_ylabel("open findings"); ax.set_ylim(0, 14); ax.set_xlim(102, 131)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 11, data="04-code/ch36/output/retest.txt (Chapter 32 and 38 closures)")
