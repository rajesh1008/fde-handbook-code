"""Figure 21.5: the quality scorer at the door: three gated dimensions and three outcomes, with counts."""
import re
from _common import S, save, blank, text
t = text("scorer")
acc, req, rej = map(int, re.search(r"accept (\d+), request (\d+), reject (\d+)", t).groups())
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6))
S.box(ax, 0.1, 2.4, 1.8, 1.2, "document\narrives", role="data", fs=10)
for i, d in enumerate(("completeness", "legibility", "consistency")):
    S.box(ax, 2.6, 4.2 - i * 1.7, 2.6, 1.1, d, role="evidence", fs=10)
    S.arrow(ax, 1.9, 3.0, 2.6, 4.75 - i * 1.7)
    S.arrow(ax, 5.2, 4.75 - i * 1.7, 6.0, 3.0)
S.box(ax, 6.0, 2.3, 1.2, 1.4, "hard\ngates", role="system", fs=10)
outs = [(f"accept {acc:,}", "approval", "extraction"), (f"request {req}", "data", "ask the sender"), (f"reject {rej}", "blocker", "ask for a resend")]
for i, (lab, role, nxt) in enumerate(outs):
    y = 4.4 - i * 1.75
    S.box(ax, 7.9, y, 2.0, 1.0, lab, role=role, fs=10)
    S.arrow(ax, 7.2, 3.0, 7.9, y + 0.5)
    S.label(ax, 8.9, y - 0.32, nxt, fs=10, ha="center")
save(fig, 5, kind="diagram", data="04-code/ch21/output/scorer.txt")
