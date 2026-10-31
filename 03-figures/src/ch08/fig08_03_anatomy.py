"""Figure 8.3: the seven parts of a success criterion, shown on C-03."""
from _common import S, plt, save, clean
fig, ax = S.figure(4.2); clean(ax, 10, 7.2)
parts = [("statement", "fields sent without review are right", "model"),
         ("metric", "fields correct under the rubric", "model"),
         ("scorer", "Anne Kessler", "approval"),
         ("document set", "gold set, 500, by path", "data"),
         ("denominator", "fields sent without review", "data"),
         ("threshold", "98% or better", "evidence"),
         ("reported apart", "review share; per field", "evidence")]
for i, (k, v, r) in enumerate(parts):
    y = 6.3 - i * 0.95
    S.box(ax, 0.2, y, 2.6, 0.72, k, role=r, fs=10)
    S.label(ax, 3.1, y + 0.36, v, fs=10, va="center")
save(fig, 3, kind="diagram")
