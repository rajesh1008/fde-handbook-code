"""Figure 32.3: one answer as data: question, answer, claim, evidence, owner, expiry."""
from _common import S, save, blank
fig, ax = S.figure(height=4.0); blank(ax, (0, 10), (0, 6))
S.box(ax, 0.2, 4.3, 2.8, 1.1, "SQ-09\npenetration test?", role="model")
S.box(ax, 3.6, 4.3, 2.8, 1.1, "answer\nclaim: documented", role="system")
S.box(ax, 7.0, 4.3, 2.8, 1.1, "EV-07\ntest report", role="evidence")
S.box(ax, 7.0, 2.3, 2.8, 1.1, "owner\nLaura Finch", role="approval")
S.box(ax, 3.6, 2.3, 2.8, 1.1, "scope: any", role="data")
S.box(ax, 0.2, 2.3, 2.8, 1.1, "expired day 55", role="blocker", lw=S.LW["emphasis"])
S.arrow(ax, 3.0, 4.85, 3.6, 4.85); S.arrow(ax, 6.4, 4.85, 7.0, 4.85)
S.arrow(ax, 8.4, 4.3, 8.4, 3.4); S.arrow(ax, 7.0, 2.85, 6.4, 2.85); S.arrow(ax, 3.6, 2.85, 3.0, 2.85)
S.label(ax, 0.2, 1.2, "checked on the review day: register, date, scope, owner, claim", fs=10)
save(fig, 3, kind="diagram", data="04-code/ch32/world.py (SQ-09, EV-07)")
