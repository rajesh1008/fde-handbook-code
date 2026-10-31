"""Figure 44.10: monthly load index per person, with the red threshold."""
from _common import S, save, text
L = text("rotation").splitlines()[2:10]
fig, ax = S.figure(height=4.2)
style = {"Maya Brooks": ("blocker", S.LW["emphasis"], "-"), "Callum Reid": ("data", 1.5, "-"), "lead FDE": ("model", 1.5, "-")}
for l in L:
    parts = l.split(); vals = parts[-12:]; name = " ".join(parts[:-12])
    xs = [i + 1 for i, v in enumerate(vals) if v != "."]; ys = [float(v) for v in vals if v != "."]
    if len(xs) < 2:
        continue
    r, lw, ls = style.get(name, ("evidence", 0.75, "--"))
    ax.plot(xs, ys, color=S.ROLE[r], lw=lw, ls=ls, marker="o", ms=3, label=name if name in style else None)
ax.plot([], [], color=S.ROLE["evidence"], lw=0.75, ls="--", label="others")
ax.axhline(3.0, color=S.ROLE["blocker"], lw=0.75, ls=":"); ax.text(1, 3.08, "red: 3.0 for two months", fontsize=9)
ax.axvline(11, color=S.PAL["ink"], lw=0.75); ax.text(10.9, 4.6, "leaves", fontsize=9, ha="right")
ax.set_xticks(range(1, 13)); ax.set_xlabel("function month"); ax.set_ylabel("load index"); ax.set_ylim(0, 5.2)
ax.legend(loc="upper left", fontsize=9, bbox_to_anchor=(0, 0.9)); ax.spines[["top", "right"]].set_visible(False)
save(fig, 10, data="04-code/ch44/output/rotation.txt")
