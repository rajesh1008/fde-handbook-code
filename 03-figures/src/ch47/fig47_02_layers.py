"""Figure 47.2: four layers of an engagement: product, platform, playbooks, and what never repeats."""
from _common import S, save, blank
fig, ax = S.figure(height=4.6); blank(ax, (0, 10), (0, 8))
L = [(6.1, "product", "model", "features shipped from the field"),
     (4.2, "platform", "system", "gateway adapter, evaluation suite, audit log"),
     (2.3, "playbooks", "data", "claims, reconciliation, referral, model access"),
     (0.4, "never repeats", "blocker", "system-of-record connector, sponsor view")]
for y, t, r, sub in L:
    S.box(ax, 0.2, y, 2.6, 1.5, t, role=r, fs=10)
    S.box(ax, 3.2, y, 6.6, 1.5, sub, role=r, fs=9)
S.arrow(ax, 1.5, 2.0, 1.5, 2.3, weight="emphasis"); S.arrow(ax, 1.5, 3.9, 1.5, 4.2, weight="emphasis")
S.arrow(ax, 1.5, 5.8, 1.5, 6.1, weight="emphasis")
save(fig, 2, kind="diagram", data="04-code/ch47/output/repeats.txt; world.py playbooks")
