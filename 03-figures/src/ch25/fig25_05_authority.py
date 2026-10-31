"""Figure 25.5: the two authority rulings side by side: Anne Kessler's refusals at Caldwell, Michael Hart's at Greystone."""
from _common import S, save, blank
fig, ax = S.figure(height=4.0)
blank(ax, (0, 10), (0, 6))
S.label(ax, 2.45, 5.6, "Anne Kessler, Caldwell", fs=10.5, ha="center", weight="bold")
S.label(ax, 7.55, 5.6, "Michael Hart, Greystone", fs=10.5, ha="center", weight="bold")
for j, t in enumerate(("set a reserve", "set claim status", "assign an adjuster")):
    S.box(ax, 0.3, 4.3 - j * 1.1, 4.3, 0.8, t, role="blocker", fs=10)
for j, t in enumerate(("submit to a payer", "set urgency", "message a patient")):
    S.box(ax, 5.4, 4.3 - j * 1.1, 4.3, 0.8, t, role="blocker", fs=10)
S.box(ax, 0.3, 0.2, 4.3, 0.8, "draft and preprod write", role="approval", fs=10)
S.box(ax, 5.4, 0.2, 4.3, 0.8, "draft only; red flags to clinician", role="approval", fs=10)
save(fig, 5, kind="diagram", data="04-code/ch25/policy.py")
