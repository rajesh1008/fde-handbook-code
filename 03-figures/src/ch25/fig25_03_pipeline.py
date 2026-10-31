"""Figure 25.3: propose, authorize, execute, verify, with the five authorizer stages; deny by default."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4)
blank(ax, (0, 10), (0, 6.4))
steps = [("propose", "model"), ("authorize", "evidence"), ("execute", "system"), ("verify", "approval")]
for i, (s, r) in enumerate(steps):
    x = 0.1 + i * 2.5
    S.box(ax, x, 5.0, 2.1, 0.9, s, role=r, fs=10.5)
    if i < 3:
        S.arrow(ax, x + 2.1, 5.45, x + 2.5, 5.45)
for j, st in enumerate(("boundary", "protected fields", "finality", "values", "intent key")):
    y = 3.9 - j * 0.75
    S.box(ax, 2.6, y, 2.1, 0.6, st, role="evidence", fs=9.5)
    S.arrow(ax, 4.7, y + 0.3, 5.6, y + 0.3, ls="--", weight="data")
    S.label(ax, 5.7, y + 0.3, "deny, record", fs=9.5, ha="left", va="center")
S.arrow(ax, 3.65, 5.0, 3.65, 4.5)
S.box(ax, 7.6, 2.2, 2.3, 1.1, "action record\nfor every step", role="evidence", fs=10)
S.arrow(ax, 8.75, 5.0, 8.75, 3.3)
save(fig, 3, kind="diagram", data="04-code/fieldkit/fieldkit/actions.py")
