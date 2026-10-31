"""Figure 25.14: the model's description against the payload: the review screen draws the payload."""
import re
from _common import S, save, blank, text
t = text("review_surface")
mism, hidden = map(int, re.search(r"payload: (\d+)\s+of which .* is wrong: (\d+)", t).groups())
fig, ax = S.figure(height=4.0)
blank(ax, (0, 10), (0, 6))
S.box(ax, 0.2, 3.9, 4.4, 1.5, "model says:\nclaimant Susan Lopez", role="model", fs=10)
S.box(ax, 5.4, 3.9, 4.4, 1.5, "will write:\nclaimant Susan", role="blocker", fs=10, mono=False)
S.box(ax, 0.2, 0.6, 9.6, 1.6, f"description disagreed with payload {mism} times;\n{hidden} looked right while the payload was wrong",
      role="evidence", fs=10)
S.label(ax, 2.4, 3.4, "not shown for approval", fs=9.5, ha="center")
S.label(ax, 7.6, 3.4, "shown, flagged against the letter", fs=9.5, ha="center")
save(fig, 14, kind="diagram", data="04-code/ch25/output/review_surface.txt")
