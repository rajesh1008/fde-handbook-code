"""Figure 24.2: the four options, by where the surface and the brain sit and how many calls cross per turn."""
import re
from _common import S, save, blank, text
cross = re.search(r"would make (\d+) crossings per turn", text("split")).group(1)
fig, ax = S.figure(height=4.2)
blank(ax, (0, 10), (0, 6))
ax.axhline(3.0, color=S.PAL["ink"], lw=S.LW["emphasis"], ls=(0, (2, 3)))
S.label(ax, 0.3, 3.12, "suite", fs=10, weight="bold"); S.label(ax, 0.3, 2.62, "Caldwell cloud", fs=10, weight="bold")
opts = [("A new app", "cloud", "cloud", ""), ("B suite agent", "suite", "suite", ""),
        ("C hybrid", "suite", "cloud", "1 call"), ("D suite orchestration", "suite", "cloud", f"{cross} calls")]
for i, (name, surf, brain, lab) in enumerate(opts):
    x = 0.3 + i * 2.45
    S.label(ax, x + 1.0, 5.6, name, fs=10, ha="center", weight="bold")
    ys = 3.9 if surf == "suite" else 1.6
    yb = 3.9 if brain == "suite" else 1.6
    if surf == brain:
        top = 4.4 if surf == "suite" else 1.7
        S.box(ax, x, top, 2.0, 0.8, "surface", role="system", fs=10)
        S.box(ax, x, top - 1.1, 2.0, 0.8, "brain", role="model", fs=10)
    else:
        big = i == 3
        S.box(ax, x, 3.9, 2.0, 0.8 if not big else 1.3, "surface" if not big else "surface +\norchestration", role="system", fs=10)
        S.box(ax, x, 1.6, 2.0, 0.8, "brain" if not big else "tools", role="model", fs=10)
        n = 1 if i == 2 else 4
        for k in range(n):
            xx = x + 1.0 + (k - (n - 1) / 2) * 0.35
            S.arrow(ax, xx, 3.9, xx, 2.4, color=S.ROLE["blocker"] if big else S.PAL["ink"],
                    weight="emphasis" if not big else "control")
        S.label(ax, x + 1.0, 3.12 if not big else 2.65, lab, fs=10, ha="center", weight="bold",
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))
save(fig, 2, kind="diagram", data="04-code/ch24/output/split.txt")
