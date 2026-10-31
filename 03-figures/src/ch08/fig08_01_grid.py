"""Figure 8.1: scope as document types x decisions, with monthly volumes (signed scope v1.0, day 28)."""
from _common import S, plt, save, clean
import caldwell_scope as cs
doc = cs.signed()
fig, ax = S.figure(3.9); clean(ax, 10, 6.4)
keys = list(doc.decisions)
heads = ["type", "fields", "route", "hold"]
cols = ["K1", "K2", "K3", "K4", "K5"]
lab = ["classify", "match", "fields", "route", "hold"]
for j, l in enumerate(lab):
    S.label(ax, 4.3 + j * 1.15, 5.9, l, fs=9.5, ha="center")
for i, t in enumerate(doc.doc_types):
    y = 4.9 - i * 1.15
    S.label(ax, 0, y + 0.42, f"{t.name}", fs=9.5, va="center")
    S.label(ax, 0, y + 0.02, f"{t.volume:,} a month", fs=9, va="center")
    for j, k in enumerate(cols):
        on = k in t.decisions
        S.box(ax, 3.85 + j * 1.15, y, 0.9, 0.8, "yes" if on else "no", role="system" if on else "evidence",
              fs=9.5, hatch=on)
save(fig, 1, kind="diagram")
