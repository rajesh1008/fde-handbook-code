"""Figure 31.6: the 289 disagreements by adjudicated cause (shadow_run.txt)."""
from _common import S, save, text
t = text("shadow_run").split("disagreements by cause")[1].split("\n\n")[0].splitlines()[1:]
rows = [(l.rsplit(None, 1)[0].strip(), int(l.split()[-1])) for l in t if l.strip()]
fig, ax = S.figure(height=3.8)
for i, (n, v) in enumerate(rows):
    role = "evidence" if ("clerk" in n or "equivalent" in n) else "blocker"
    ax.barh(i, v, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white"); S.label(ax, v + 2, i, str(v), fs=9, va="center")
ax.set_yticks(range(len(rows)), [n for n, _ in rows], fontsize=9); ax.invert_yaxis(); ax.set_xlim(0, 150)
ax.set_xlabel("documents (agent wrong: coral; agent not wrong: slate)"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 6, data="04-code/ch31/output/shadow_run.txt")
