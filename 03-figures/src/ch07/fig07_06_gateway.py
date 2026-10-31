"""Figure 7.6: identity and audit after day 24. The agent acts for a named adjuster; the gateway stamps that
adjuster on every claims-core read; the audit table snapshot keeps before-and-after values."""
from _common import S, plt, save, clean
fig, ax = S.figure(3.8); clean(ax)
S.box(ax, 0.2, 4.6, 2.2, 1.6, "adjuster\nTom Whitfield", role="approval")
S.box(ax, 2.9, 4.6, 2.0, 1.6, "intake\nagent", role="model")
S.box(ax, 5.4, 4.6, 2.0, 1.6, "model\ngateway", role="system")
S.box(ax, 7.9, 4.6, 1.9, 1.6, "claims-\ncore", role="data")
for a, b_ in ((2.4, 2.9), (4.9, 5.4), (7.4, 7.9)):
    S.arrow(ax, a, 5.4, b_, 5.4)
S.box(ax, 5.4, 1.2, 4.4, 1.8, "read log: acting for\nadjuster, purpose, fields", role="evidence")
S.arrow(ax, 6.4, 4.6, 6.4, 3.0, weight="data")
S.box(ax, 0.2, 1.2, 4.4, 1.8, "weekly audit-table\nsnapshot", role="evidence")
S.arrow(ax, 8.8, 4.6, 3.2, 3.0, weight="data")
save(fig, 6, kind="diagram")
