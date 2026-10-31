"""Figure 40.2: the five questions an auditor asks, in the order asked, and the pack elements that answer each."""
from _common import S, save, blank
fig, ax = S.figure(height=4.9); blank(ax, (0, 10), (0, 10))
rows = [("what was decided?", "decision, action"), ("from what input?", "document, lineage, retrieval"),
        ("under which rules?", "prompt, model, route"), ("who checked it?", "review"), ("show it again", "chain head")]
for i, (q, a) in enumerate(rows):
    y = 8.3 - i * 1.9
    S.box(ax, 0.1, y, 3.9, 1.3, q, role="evidence", fs=10)
    S.box(ax, 5.4, y, 4.5, 1.3, a, role="approval", fs=10)
    S.arrow(ax, 4.0, y + 0.65, 5.4, y + 0.65)
save(fig, 2, kind="diagram", data="04-code/ch40/pack.py ELEMENTS; Section 40.1")
