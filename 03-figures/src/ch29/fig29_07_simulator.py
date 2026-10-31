"""Figure 29.7: the scenario simulator at layer four (Listing 29.5)."""
from _common import S, save, blank
fig, ax = S.figure(height=4.2)
blank(ax, (0, 10), (0, 7))
S.box(ax, 0.2, 5.6, 3.0, 1.0, "template + variation", role="data")
S.box(ax, 3.9, 5.6, 2.4, 1.0, "agent under test", role="model")
S.box(ax, 7.0, 5.6, 2.8, 1.0, "end state", role="data")
S.arrow(ax, 3.2, 6.1, 3.9, 6.1); S.arrow(ax, 6.3, 6.1, 7.0, 6.1)
sims = [(0.2, "claims-core stub"), (3.5, "gateway: 429,\nkey rotation"), (6.8, "mailroom: duplicates,\npage order")]
for x, t in sims:
    S.box(ax, x, 3.4, 3.0, 1.2, t, role="system", fs=9.5)
    S.arrow(ax, 5.1, 5.6, x + 1.5, 4.6, weight="data")
S.box(ax, 7.0, 1.6, 2.8, 1.0, "oracle: expected state", role="evidence", fs=9.5)
S.arrow(ax, 8.4, 5.6, 8.4, 4.6, weight="data")
S.box(ax, 0.2, 1.6, 5.6, 1.0, "mismatch goes to triage", role="blocker", fs=10)
S.arrow(ax, 7.0, 2.1, 5.8, 2.1)
for x, t in ((0.2, "agent defect"), (2.1, "oracle defect"), (4.0, "broken scenario")):
    S.box(ax, x, 0.1, 1.8, 0.9, t, role="evidence", fs=9)
    S.arrow(ax, 3.0, 1.6, x + 0.9, 1.0, weight="data")
save(fig, 7, kind="diagram", data="04-code/ch29/common.py chk_system")
