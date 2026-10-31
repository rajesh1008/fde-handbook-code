"""Figure 40.8: replay checks the record against what was retained; rerun asks the model again and is advisory."""
from _common import S, save, blank
fig, ax = S.figure(height=4.0); blank(ax, (0, 10), (0, 8))
S.label(ax, 0.1, 7.3, "replay: proof", fs=10.5, weight="bold")
for i, (t, r) in enumerate((("run record", "data"), ("check hashes", "evidence"), ("pack holds", "approval"))):
    S.box(ax, 0.1 + i * 3.4, 4.9, 2.8, 1.6, t, role=r, fs=10)
    if i: S.arrow(ax, i * 3.4 - 0.5, 5.7, i * 3.4 + 0.1, 5.7)
S.label(ax, 0.1, 3.3, "rerun: advisory", fs=10.5, weight="bold")
for i, (t, r) in enumerate((("same inputs", "data"), ("model again", "model"), ("agree or not", "evidence"))):
    S.box(ax, 0.1 + i * 3.4, 0.9, 2.8, 1.6, t, role=r, fs=10)
    if i: S.arrow(ax, i * 3.4 - 0.5, 1.7, i * 3.4 + 0.1, 1.7)
save(fig, 8, kind="diagram", data="04-code/ch40/pack.py (replay); rerun.py (rerun)")
