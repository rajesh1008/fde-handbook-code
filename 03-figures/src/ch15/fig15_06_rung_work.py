"""Figure 15.6: what each rung lets you build, and the only claim it lets you make."""
from _common import S, save, blank
cols = [("synthetic", "pipeline skeleton\nfailure tests", "the plumbing runs"),
        ("sampled", "readiness report\nexpert-scored set", "accuracy on\na named set"),
        ("shadowed", "live feed, no action\nagreement counts", "agreement with\nthe experts"),
        ("live", "decisions acted on\noutcome tracking", "outcomes in\nproduction")]
fig, ax = S.figure(height=3.9); blank(ax, (0, 10), (0, 6.2))
w = 2.3
for i, (rung, build, claim) in enumerate(cols):
    x = 0.1 + i * 2.48
    S.box(ax, x, 5.0, w, 0.8, rung, role="evidence", hatch=False, lw=S.LW["emphasis"], fs=11)
    S.box(ax, x, 2.6, w, 1.9, build, role="system", fs=9.5)
    S.box(ax, x, 0.3, w, 1.7, claim, role="approval", fs=10)
    S.arrow(ax, x + w / 2, 4.95, x + w / 2, 4.55); S.arrow(ax, x + w / 2, 2.55, x + w / 2, 2.05)
save(fig, 6, kind="diagram", data="04-code/fieldkit histories.RUNG_WORK")
