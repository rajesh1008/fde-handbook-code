"""Figure 33.8: pack v1 against pack v2, metric by metric; M4 and M6 needed Northlight."""
import re
from _common import S, save, blank, text
t = text("monitor")
v1 = re.findall(r"^  (M\d) .*?(OK|NEEDS NORTHLIGHT)$", t.split("pack v2")[0], re.M)
v2 = re.findall(r"^  (M\d) .*?(OK|NEEDS NORTHLIGHT)$", t.split("pack v2")[1], re.M)
fig, ax = S.figure(height=4.2); blank(ax, (0, 10), (0, 7.2))
S.label(ax, 2.4, 6.8, "pack v1, day 140", ha="center", fs=10); S.label(ax, 7.6, 6.8, "pack v2, day 144", ha="center", fs=10)
for col, rows in ((0.4, v1), (5.6, v2)):
    for i, (m, s) in enumerate(rows):
        ok = s == "OK"
        S.box(ax, col, 5.6 - i * 1.05, 4.0, 0.85, f"{m}  {'Caldwell' if ok else 'needs Northlight'}",
              role="approval" if ok else "blocker", lw=S.LW["control"] if ok else S.LW["emphasis"], fs=9.5)
save(fig, 8, kind="diagram", data="04-code/ch33/output/monitor.txt")
