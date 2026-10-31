"""Figure 8.12: the scoping document as code: one source, a lint gate, three outputs."""
from _common import S, plt, save, clean
fig, ax = S.figure(4.2); clean(ax, 10, 7)
S.box(ax, 0.2, 5.4, 4.0, 1.2, "discovery log, bank\n(Chapters 6, 7)", role="data", fs=10)
S.box(ax, 5.6, 5.4, 4.2, 1.2, "deal sheet, kickoff\n(vendor documents)", role="blocker", fs=10)
S.box(ax, 2.6, 3.3, 4.8, 1.2, "ScopeDoc\nclaims with statuses", role="model", fs=10)
S.arrow(ax, 2.2, 5.4, 3.6, 4.5); S.arrow(ax, 7.7, 5.4, 6.4, 4.5)
S.box(ax, 3.4, 1.9, 3.2, 0.8, "lint: 0 findings", role="approval", fs=10, lw=S.LW["emphasis"])
S.arrow(ax, 5.0, 3.3, 5.0, 2.7, weight="emphasis")
for i, t in enumerate(["signed document\nwith strips", "evaluation suite\nconfig\n7 criteria", "decision register\n7 records"]):
    x = 0.2 + i * 3.3
    S.box(ax, x, 0.1, 3.0, 1.2, t, role="evidence", fs=10)
    S.arrow(ax, 5.0, 1.9, x + 1.5, 1.3)
save(fig, 12, kind="diagram")
