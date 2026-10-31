"""Figure 34.3: where the data goes, Caldwell (all hops covered by v5) and Greystone (one hop uncovered on day 108)."""
from _common import S, save, blank
fig, ax = S.figure(height=4.9); blank(ax, (0, 10), (0, 8))
cal = [("claim files\nS3, us-east-1", "data"), ("runner in\nCaldwell's account", "system"),
       ("Caldwell\ngateway", "system"), ("model\nprovider", "model")]
for i, (t, r) in enumerate(cal):
    S.box(ax, 0.1 + i * 2.5, 5.2, 2.1, 1.6, t, role=r, fs=9.5)
    if i:
        S.arrow(ax, i * 2.5 - 0.3, 6.0, i * 2.5 + 0.1, 6.0)
ax.text(0.1, 7.3, "Caldwell v5: 6 hops, 6 covered", fontsize=10, fontweight="bold")
gs = [("referrals\nGreystone tenant", "data"), ("drafting\nservice", "system"), ("model\nprovider", "model"),
      ("abuse-monitoring\nstore: uncovered", "blocker")]
for i, (t, r) in enumerate(gs):
    S.box(ax, 0.1 + i * 2.5, 1.2, 2.1, 1.6, t, role=r, fs=9.5, lw=2.5 if r == "blocker" else None)
    if i:
        S.arrow(ax, i * 2.5 - 0.3, 2.0, i * 2.5 + 0.1, 2.0)
ax.text(0.1, 3.3, "Greystone day 108: 4 hops, 1 uncovered (F-10)", fontsize=10, fontweight="bold")
save(fig, 3, kind="diagram", data="04-code/ch34/output/dataterms.txt")
