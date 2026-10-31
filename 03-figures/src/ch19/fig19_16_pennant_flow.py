"""Figure 19.16: Pennant's status path: EDI all day, the CSV at 02:00, reconciled every night."""
from _common import S, save, blank
fig, ax = S.figure(height=4.2)
blank(ax, (0, 12), (0, 7))
S.box(ax, 0.2, 4.6, 2.6, 1.4, "carrier\nEDI 214", role="data", fs=10)
S.box(ax, 3.6, 4.6, 2.8, 1.4, "parse,\nenvelope check", role="system", fs=10)
S.box(ax, 7.2, 4.6, 2.8, 1.4, "intraday\nstatus", role="model", fs=10)
S.box(ax, 0.2, 1.2, 2.6, 1.4, "TMS CSV\n02:00", role="data", fs=10)
S.box(ax, 3.6, 1.2, 2.8, 1.4, "file drop\nchecks", role="system", fs=10)
S.box(ax, 7.2, 1.2, 2.8, 1.4, "reconcile", role="evidence", fs=10)
for y in (5.3, 1.9):
    S.arrow(ax, 2.8, y, 3.6, y); S.arrow(ax, 6.4, y, 7.2, y)
S.arrow(ax, 8.6, 4.6, 8.6, 2.6)
S.arrow(ax, 10.0, 1.9, 11.3, 1.9); S.label(ax, 10.2, 2.3, "differences\nto clerks", fs=9.5)
save(fig, 16, kind="diagram", data="04-code/ch19/pennant_edi.py")
