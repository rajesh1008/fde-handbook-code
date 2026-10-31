"""Figure 44.12: the five-level ladder, with the evidence each step adds."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4); blank(ax, (0, 10), (0, 6.4))
lv = [("FDE I", "learns the six verbs on one account", "evidence"),
      ("FDE II", "one workstream to Build Complete", "data"),
      ("Senior FDE", "leads a gate and a hand-over", "system"),
      ("Staff FDE", "two customers led; playbook reused", "model"),
      ("Principal FDE", "changes the practice", "approval")]
for i, (n, t, r) in enumerate(lv):
    x, y = 0.3 + i * 1.0, 0.3 + i * 1.2
    S.box(ax, x, y, 2.1, 0.8, n, role=r, fs=9)
    S.label(ax, x + 2.35, y + 0.28, t, fs=9)
    if i:
        S.arrow(ax, x + 0.3, y - 0.4, x + 0.3, y, weight="control")
save(fig, 12, kind="diagram", data="04-code/ch44/world.py CRITERIA")
