"""Figure 43.5: hours Pennant would need to run the system alone from each month. Data: model_pennant.txt."""
from _common import S, save, months, PATH_STYLE, endlabels
d = months("pennant")
fig, ax = S.figure(height=3.9)
for k, (role, ls, lab) in PATH_STYLE.items():
    t = d[k]["takeover"]
    ax.step(range(1, 25), t, where="mid", color=S.ROLE[role], ls=ls, lw=S.LW["emphasis"] if k == "managed" else S.LW["control"])
endlabels(ax, [(d[k]['takeover'][-1], PATH_STYLE[k][2]) for k in PATH_STYLE], 35)
ax.set_xlim(0.5, 33); ax.set_ylim(0, 900); ax.set_xticks([1, 6, 12, 18, 24])
ax.set_xlabel("month of the model"); ax.set_ylabel("takeover hours")
save(fig, 5, data="04-code/ch43/output/model_pennant.txt (MONTHS)")
