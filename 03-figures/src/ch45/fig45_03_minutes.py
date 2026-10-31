"""Figure 45.3: candidate time and observed competency per round, v0 against v1."""
from _common import S, save, coverage, COMPS
v0, v1 = coverage("loop_v0"), coverage("loop_v1")
fig, ax = S.figure(height=4.4)
roles = dict(discovery="model", decomposition="system", build="data", judgment="approval", communication="evidence")
y = 0; ticks = []
for name, rows in (("v1", v1[::-1]), ("v0", v0[::-1])):
    for r in rows:
        obs = [c for c, v in zip(COMPS, r[1]) if v == "obs"]
        left = 0
        share = r[2] / max(1, len(obs))
        for c in obs:
            ax.barh(y, share, left=left, color=S.ROLE[roles[c]], hatch=S.HATCH[roles[c]], edgecolor="white", height=0.7)
            left += share
        if not obs:
            ax.barh(y, r[2], color="white", edgecolor=S.PAL["ink"], hatch="", height=0.7, ls="--")
        ticks.append((y, f"{name} {r[0]}"))
        y += 1
    y += 0.6
ax.set_yticks([t[0] for t in ticks]); ax.set_yticklabels([t[1] for t in ticks], fontsize=9.5)
ax.set_xlabel("candidate minutes (bar split by competency observed)")
for c in COMPS:
    ax.barh(-5, 0, color=S.ROLE[roles[c]], hatch=S.HATCH[roles[c]], label=c)
ax.barh(-5, 0, color="white", edgecolor=S.PAL["ink"], ls="--", label="nothing observed")
ax.set_ylim(-0.6, y - 0.4); ax.legend(fontsize=9, loc="lower right"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 3, data="04-code/ch45/output/loop_v0.txt, loop_v1.txt")
