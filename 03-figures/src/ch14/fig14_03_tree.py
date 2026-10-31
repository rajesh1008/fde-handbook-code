"""Figure 14.3: the decision tree applied to the 25 electronic steps (diagram)."""
from _common import S, save, plt, blank, CLASS_ROLE
import pipeline as pl
from decision_tree import CLASSES, split

sp = split(pl.ELECTRONIC)
fig, ax = S.figure(4.4)
blank(ax, (0, 10), (0, 7.2))
qs = ["Output fixed by lookup,\ncalculation or record write?", "Written rules with\na named owner?",
      "Closed output a check\ncan verify?"]
names = ["deterministic service", "rules + guardrails", "small model", "frontier + retrieval"]
ys = [6.0, 4.2, 2.4]
for i, (q, y) in enumerate(zip(qs, ys)):
    S.box(ax, 0.2, y - 0.5, 4.2, 1.0, q, role="evidence", fs=9.5)
    S.box(ax, 6.0, y - 0.5, 3.8, 1.0, f"{names[i]}: {sp[CLASSES[i]]}", role=CLASS_ROLE[i], fs=10)
    S.arrow(ax, 4.4, y, 6.0, y); S.label(ax, 4.95, y + 0.12, "yes", fs=9.5)
    if i < 2:
        S.arrow(ax, 2.3, y - 0.5, 2.3, ys[i + 1] + 0.5); S.label(ax, 2.45, y - 0.95, "no", fs=9.5)
S.arrow(ax, 2.3, 1.9, 2.3, 1.1); S.label(ax, 2.45, 1.45, "no", fs=9.5)
S.arrow(ax, 2.3, 0.6, 6.0, 0.6)
S.box(ax, 6.0, 0.1, 3.8, 1.0, f"{names[3]}: {sp[CLASSES[3]]}", role=CLASS_ROLE[3], fs=10)
S.label(ax, 0.2, 0.25, "16 of 25 = 64%\nneed no model", fs=10, weight="bold")
save(fig, 3, kind="diagram")
