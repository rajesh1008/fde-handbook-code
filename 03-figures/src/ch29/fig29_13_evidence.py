"""Figure 29.13: test evidence chained from requirement to gate (Listing 29.10)."""
from _common import S, save, blank
fig, ax = S.figure(height=4.0)
blank(ax, (0, 10), (0, 6.4))
steps = [("requirement", "data"), ("check", "system"), ("run: commit, layer", "model"), ("result: verdict", "evidence")]
for i, (t, r) in enumerate(steps):
    x = 0.1 + i * 2.5
    S.box(ax, x, 4.8, 2.2, 1.0, t, role=r, fs=9.5)
    if i:
        S.arrow(ax, x - 0.3, 5.3, x, 5.3)
for i in range(3):
    x = 0.6 + i * 3.1
    S.box(ax, x, 2.4, 2.5, 1.1, f"record {i + 1}\nhash of record\n+ previous hash", role="evidence", fs=9)
    if i:
        S.arrow(ax, x - 0.6, 2.95, x, 2.95)
S.arrow(ax, 8.6, 4.8, 8.4, 3.5, weight="data")
S.box(ax, 2.0, 0.3, 6.0, 1.0, "gate evidence pack: write-once store", role="approval", fs=10)
S.arrow(ax, 5.0, 2.4, 5.0, 1.3)
save(fig, 13, kind="diagram", data="fieldkit/pyramid.py EvidenceRecord, chain")
