"""Figure 15.3: the day-3 email and the day-9 record asked for the same files; only the record had an owner, a queue and a date."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9); blank(ax, (0, 10), (0, 6.2))
S.box(ax, 0.2, 4.9, 4.4, 0.9, "day 3: email", role="evidence", hatch=False, lw=S.LW["emphasis"])
S.box(ax, 5.4, 4.9, 4.4, 0.9, "day 9: intake record", role="evidence", hatch=False, lw=S.LW["emphasis"])
S.box(ax, 0.2, 2.3, 4.4, 2.0, "\"sample data\"\nno owner, no purpose\nno readers, no storage", role="blocker")
S.box(ax, 5.4, 2.3, 4.4, 2.0, "sponsor Anne Kessler\npurpose, named readers\nbank details redacted", role="approval")
S.box(ax, 0.2, 0.3, 4.4, 1.2, "nothing", role="blocker", hatch=False)
S.box(ax, 5.4, 0.3, 4.4, 1.2, "200 files, day 47", role="data")
for x in (2.4, 7.6):
    S.arrow(ax, x, 4.85, x, 4.35); S.arrow(ax, x, 2.25, x, 1.55)
save(fig, 3, kind="diagram", data="Chapter 3 (day-3 email, day-9 intake request)")
