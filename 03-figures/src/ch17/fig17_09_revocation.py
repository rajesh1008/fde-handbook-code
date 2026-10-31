"""Figure 17.13: Pennant disables a key version; the runner fails closed and says why."""
from _common import S, save, blank
fig, ax = S.figure(height=3.8)
blank(ax, (0, 10), (0, 6))
steps = (("Pennant disables\nkey version", "blocker"), ("decrypt\ndenied", "data"), ("runner stops\nreads, says why", "system"),
         ("alert: Pennant\nand Northlight", "evidence"), ("new version,\nrunner resumes", "approval"))
for i, (lab, role) in enumerate(steps):
    x = 0.05 + i * 2.0
    S.box(ax, x, 2.4, 1.8, 1.5, lab, role=role, fs=9.5)
    if i: S.arrow(ax, x - 0.2, 3.15, x, 3.15)
S.label(ax, 0.05, 1.3, "the customer's key is its off switch; design for it", fs=10, color=S.PAL["slate"])
save(fig, 9, kind="diagram", data="chapter text (Pennant)")
