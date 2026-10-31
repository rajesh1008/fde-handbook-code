"""Figure 15.7: the same seven deterministic stages on synthetic and real files; two stages move, both because of the data."""
import io, contextlib, runpy
from _common import S, save, R
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    g = runpy.run_path(str(R / "04-code/ch15/plumbing_check.py"))
syn, real, STAGES = g["a"], g["b"], g["STAGES"]
fig, ax = S.figure(height=4.2)
names = [n for n, _ in STAGES]
for i, n in enumerate(names):
    y = len(names) - 1 - i
    ax.barh(y + 0.18, syn[n] / 2, height=0.34, color=S.TINT["system"], hatch=S.HATCH["system"], edgecolor=S.ROLE["system"], lw=S.LW["data"])
    moved = abs(syn[n] - real[n]) >= 2
    ax.barh(y - 0.18, real[n] / 2, height=0.34, color=S.ROLE["data"], edgecolor=S.PAL["ink"] if moved else S.ROLE["data"],
            lw=S.LW["emphasis"] if moved else S.LW["data"])
    ax.text(real[n] / 2 + 1, y - 0.18, f"{real[n] / 2:.1f}%", va="center", fontsize=9.5, color=S.PAL["ink"])
ax.set_yticks(range(len(names))); ax.set_yticklabels(list(reversed(names)), fontsize=9.5)
ax.set_xlim(0, 118); ax.set_xticks([0, 25, 50, 75, 100]); ax.set_xlabel("files passing the stage (%)")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=S.TINT["system"], hatch=S.HATCH["system"], edgecolor=S.ROLE["system"], label="synthetic"),
                   Patch(facecolor=S.ROLE["data"], edgecolor=S.ROLE["data"], label="real sample")],
          loc="lower right", frameon=True, edgecolor=S.PAL["light"])
save(fig, 7, data="04-code/ch15 plumbing_check.py")
