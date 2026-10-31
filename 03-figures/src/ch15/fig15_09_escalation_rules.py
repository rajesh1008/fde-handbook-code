"""Figure 15.9: the escalation rules; one level at a time, counted in days the customer has had the next move."""
from _common import S, save, blank
fig, ax = S.figure(height=4.0); blank(ax, (0, 10), (-0.9, 5.8))
lv = [("level 1: dated ask to the owner", "agreed time passed, or work starts in 3 days", 0.2, 4.9),
      ("level 2: sponsor, owner copied", "two weeks past agreed, work blocked", 1.4, 3.1),
      ("level 3: steering agenda item", "twice agreed, planned work late", 2.6, 1.3)]
for title, rule, x, y in lv:
    S.box(ax, x, y, 7.2, 0.7, title, role="evidence", hatch=False, lw=S.LW["emphasis"])
    S.box(ax, x, y - 0.7, 7.2, 0.7, rule, role="evidence")
for (_, _, x, y), (_, _, x2, y2) in zip(lv, lv[1:]):
    S.arrow(ax, x2 + 0.6, y - 0.7, x2 + 0.6, y2 + 0.7)
S.box(ax, 0.2, -0.8, 4.4, 0.75, "our move: never escalated", role="blocker", lw=S.LW["emphasis"])
save(fig, 9, kind="diagram", data="04-code/fieldkit escalation.EscalationPolicy.rule_level")
