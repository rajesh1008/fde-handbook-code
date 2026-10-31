"""Figure 35.8: the data-map method: configuration in, a digest the approver can reproduce out."""
from _common import S, save, blank
fig, ax = S.figure(height=4.9); blank(ax, (0, 10), (0, 8))
top = [("deployed\nconfiguration", "system"), ("generate\nhops", "evidence"), ("lint per\nregime", "blocker")]
low = [("scan the\nstores", "data"), ("digest", "evidence"), ("owner reruns\nand signs", "approval")]
for i, (t, r) in enumerate(top):
    S.box(ax, 0.2 + i * 3.4, 5.4, 2.8, 1.8, t, role=r, fs=10)
    if i:
        S.arrow(ax, i * 3.4 - 0.4, 6.3, i * 3.4 + 0.2, 6.3)
for i, (t, r) in enumerate(low):
    S.box(ax, 7.0 - i * 3.4, 1.4, 2.8, 1.8, t, role=r, fs=10)
    if i:
        S.arrow(ax, 7.0 - (i - 1) * 3.4, 2.3, 7.0 - i * 3.4 + 2.8, 2.3)
S.arrow(ax, 8.4, 5.4, 8.4, 3.2)
S.arrow(ax, 1.6, 3.2, 1.6, 5.4, ls="--", color=S.PAL["grey"])
S.label(ax, 2.3, 4.3, "every deploy", fs=9.5)
save(fig, 8, kind="diagram", data="04-code/ch35 (datamap.py, pii_scan.py); fieldkit/privacy.py")
