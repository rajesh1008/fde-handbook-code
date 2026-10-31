"""Figure 7.2: the four parts of one bank question (R11), and what each part is for."""
from _common import S, plt, save, clean
fig, ax = S.figure(3.8); clean(ax)
S.box(ax, 0.2, 5.3, 9.6, 1.3, "Which field holds the date\na first notice was received?", role="model", fs=11)
parts = [("why", "the clock starts\non this date", "system"), ("expected", "received_at\nvendor position", "blocker"),
         ("listen for", "next-day scans\nforwarded faxes", "data"), ("if different", "date check\nchanges", "approval")]
for i, (h, t, r) in enumerate(parts):
    x = 0.2 + i * 2.45
    S.box(ax, x, 1.2, 2.2, 2.6, f"{h}\n\n{t}", role=r, fs=10)
    S.arrow(ax, 5.0, 5.3, x + 1.1, 3.8, weight="data")
ax.text(5, 0.5, "status of the expected answer sets its weight", ha="center", fontsize=9)
save(fig, 2, kind="diagram")
