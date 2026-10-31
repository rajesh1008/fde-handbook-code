"""Figure 19.5: thirty nights of the TMS export, with the four nights the connector stopped."""
from _common import S, save
from sim import nightly_csv
fig, ax = S.figure(height=4.2)
xs, ys = [], []
for n in range(1, 31):
    if n == 26:
        continue
    c, d = nightly_csv(n, rows=18200 if n == 23 else None)
    xs.append(n); ys.append(c.count(b"\n") / 1000)
ax.plot(xs, ys, "-o", color=S.ROLE["data"], mec=S.PAL["ink"], mew=0.75, lw=S.LW["control"], ms=5)
for n, t in [(9, "re-sent"), (17, "header\nchanged"), (23, "cut off"), (26, "no file")]:
    y = dict(zip(xs, ys)).get(n, 0)
    ax.plot(n, y, "s", color=S.ROLE["blocker"], ms=9, mec=S.PAL["ink"])
    ax.annotate(t, (n, y), xytext=(n, 44 if n != 23 else 26), ha="center", fontsize=9.5,
                arrowprops=dict(arrowstyle="-", color=S.PAL["grey"], lw=0.75))
ax.set_ylim(-2, 50); ax.set_xlabel("night (September)"); ax.set_ylabel("rows (thousands)")
save(fig, 7, data="04-code/ch19/sim.py nightly_csv; 04-code/ch19/output/file_drop.txt")
