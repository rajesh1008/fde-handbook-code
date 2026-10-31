"""Figure 43.1: who does what under the three operating models. Data: the chapter's definitions (Table 43.1)."""
from _common import S, save, blank, plt  # noqa: F401
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6.2))
cols = ["hand-over", "hybrid", "managed"]
rows = [("night pager", ("customer", "customer", "vendor")), ("runbooks", ("customer", "customer", "vendor")),
        ("model change", ("customer", "both", "vendor")), ("evidence", ("customer", "customer", "both")),
        ("accountable", ("customer", "customer", "customer"))]
role = {"customer": "approval", "vendor": "cost", "both": "evidence"}
for j, c in enumerate(cols):
    S.label(ax, 3.4 + j * 2.25, 5.75, c, fs=10.5, ha="center", weight="bold")
for i, (r, cells) in enumerate(rows):
    y = 4.6 - i * 1.05
    S.label(ax, 0.1, y + 0.4, r, fs=10, va="center")
    for j, who in enumerate(cells):
        S.box(ax, 2.4 + j * 2.25, y, 2.0, 0.8, who, role=role[who], fs=10)
save(fig, 1, kind="diagram", data="02-manuscript/ch43.md Table 43.1 (definitions)")
