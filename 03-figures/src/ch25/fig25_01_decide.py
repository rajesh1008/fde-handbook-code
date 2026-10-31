"""Figure 25.2: what the Caldwell intake agent may decide, draft and do, and what stays with people and claims-core."""
from _common import S, save, blank
fig, ax = S.figure(height=4.2)
blank(ax, (0, 10), (0, 6))
cols = [("agent decides", "model", ["fields from the letter", "which document type"]),
        ("agent drafts", "evidence", ["the claim record", "a note to the adjuster"]),
        ("agent does", "approval", ["writes to preprod", "after an accept"]),
        ("never the agent", "blocker", ["reserve, status", "assignment, coverage"])]
for i, (h, role, items) in enumerate(cols):
    x = 0.1 + i * 2.5
    S.box(ax, x, 4.6, 2.3, 0.9, h, role=role, fs=10)
    for j, it in enumerate(items):
        S.label(ax, x + 1.15, 3.9 - j * 0.6, it, fs=9.5, ha="center")
    if i < 3:
        S.arrow(ax, x + 2.3, 5.05, x + 2.5, 5.05)
S.box(ax, 0.1, 0.6, 9.8, 1.0, "claims-core rules and adjusters decide the claim", role="system", fs=10)
save(fig, 1, kind="diagram", data="00-plan/ledger/ch25.md (day 104 boundary memo)")
