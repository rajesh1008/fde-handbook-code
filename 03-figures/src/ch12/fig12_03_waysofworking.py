"""Figure 12.3: the ways-of-working answer: Ready, Done and Accepted feed evidence to the gates; they never pass one."""
from _common import S, plt, save, blank
fig, ax = S.figure(3.8); blank(ax, (0, 10), (0, 6))
for x, t, txt in ((0.1, "Ready", "owner, priority,\ntestable criteria"), (3.5, "Done", "evidence\nattached"),
                  (6.9, "Accepted", "yes, dated\nfollow-up, or no")):
    S.box(ax, x, 3.6, 3.0, 1.8, f"{t}\n{txt}", role="evidence", fs=10)
S.arrow(ax, 3.1, 4.5, 3.5, 4.5); S.arrow(ax, 6.5, 4.5, 6.9, 4.5)
for i, g in enumerate(["Architecture\nReview", "Build\nComplete", "Shadow\nExit", "Model-Risk\nApproval",
                       "Live\nStable"]):
    S.box(ax, 0.1 + i * 2.0, 0.4, 1.8, 1.3, g, role="approval", fs=9)
S.arrow(ax, 8.4, 3.6, 8.4, 1.75, ls="--")
S.label(ax, 5.0, 2.55, "evidence feeds gates; acceptance never passes one", fs=9.5, ha="center")
save(fig, 3, kind="diagram")
