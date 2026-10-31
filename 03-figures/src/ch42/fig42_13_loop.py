"""Figure 42.13: the ninety-day method as a loop: detect, contain, fix and sign, review, change, drill."""
from _common import S, save, blank
import math
fig, ax = S.figure(height=5.2); blank(ax, (0, 10), (0, 8))
steps = [("detect\n(leading signal)", "data"), ("contain\n(owner's setting)", "blocker"), ("fix and\nsign", "approval"),
         ("blameless\nreview", "evidence"), ("customer\nchange", "system"), ("drill\nalone", "model")]
pos = []
for i, (t, r) in enumerate(steps):
    a = math.pi / 2 - i * 2 * math.pi / 6
    cx, cy = 5 + 3.4 * math.cos(a), 4 + 2.9 * math.sin(a)
    S.box(ax, cx - 1.25, cy - 0.6, 2.5, 1.2, t, role=r, fs=9.5); pos.append((cx, cy))
for i in range(6):
    (x1, y1), (x2, y2) = pos[i], pos[(i + 1) % 6]
    k = 0.38
    S.arrow(ax, x1 + (x2 - x1) * k, y1 + (y2 - y1) * k, x1 + (x2 - x1) * (1 - k), y1 + (y2 - y1) * (1 - k))
ax.text(5, 4, "named\ncustomer\nowner", ha="center", va="center", fontsize=10)
save(fig, 13, kind="diagram", data="Chapter 42 method; 04-code/ch42 lab")
