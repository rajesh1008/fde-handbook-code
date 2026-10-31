"""Figure 36.1: attempts per taxonomy class in the joint red team; two classes untried."""
from _common import S, save, text
rows = [l for l in text("coverage").splitlines() if l[:2] in [f"C{i}" for i in range(1, 9)]]
cls = [(l[:2], l[4:36].strip(), int(l[36:40])) for l in rows]
assert [n for *_, n in cls] == [11, 3, 4, 5, 2, 2, 0, 0]
fig, ax = S.figure(height=4.2)
y = list(range(len(cls)))[::-1]
for yi, (c, name, n) in zip(y, cls):
    if n:
        ax.barh(yi, n, 0.6, color=S.ROLE["system"])
        ax.text(n + 0.2, yi, str(n), va="center", fontsize=9.5)
    else:
        ax.barh(yi, 11, 0.6, color="white", edgecolor=S.ROLE["blocker"], hatch=S.HATCH["blocker"], lw=1.2)
        ax.text(5.5, yi, "untried", va="center", ha="center", fontsize=9.5,
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))
ax.set_yticks(y); ax.set_yticklabels([f"{c} {name}" for c, name, _ in cls], fontsize=9.5)
ax.set_xlabel("attempts, days 126 and 127"); ax.set_xlim(0, 12.5)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 1, data="04-code/ch36/output/coverage.txt")
