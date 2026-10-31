"""Figure 43.4: Pennant's hand-over readiness with use-decay, by month, four paths. Data: model_pennant.txt."""
from _common import S, save, months, PATH_STYLE, endlabels
d = months("pennant")
fig, ax = S.figure(height=3.9)
for k, (role, ls, lab) in PATH_STYLE.items():
    r = d[k]["readiness"]
    ax.step(range(1, 25), r, where="mid", color=S.ROLE[role], ls=ls, lw=S.LW["emphasis"] if k == "managed" else S.LW["control"])
endlabels(ax, [(d[k]['readiness'][-1], PATH_STYLE[k][2]) for k in PATH_STYLE], 0.04)
ax.axhline(0.6, color=S.PAL["grey"], lw=S.LW["data"], ls="--"); ax.text(1, 0.62, "gate cap 0.60", fontsize=9)
ax.set_ylim(0, 1); ax.set_xlim(0.5, 33); ax.set_xticks([1, 6, 12, 18, 24])
ax.set_xlabel("month of the model"); ax.set_ylabel("readiness")
save(fig, 4, data="04-code/ch43/output/model_pennant.txt (MONTHS)")
