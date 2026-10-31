"""Figure 7.1: the failure chain. A vendor position written as an expected answer becomes a design element,
a check and a reported number; the data owner's answer breaks the chain at the first link."""
from _common import S, plt, save, clean
fig, ax = S.figure(3.8); clean(ax)
steps = [("expected answer\nreceived_at", "blocker"), ("design v0\ndate source", "system"),
         ("date check", "model"), ("clock report", "evidence")]
for i, (t, r) in enumerate(steps):
    x = 0.2 + i * 2.5
    S.box(ax, x, 4.2, 2.0, 1.6, t, role=r, fs=10)
    if i: S.arrow(ax, x - 0.5, 5.0, x, 5.0)
S.box(ax, 0.2, 0.8, 4.5, 1.8, "day 24 data owner:\nnotice_received_dt", role="approval", fs=10)
S.arrow(ax, 1.2, 2.6, 1.2, 4.2, weight="emphasis", color=S.ROLE["approval"])
S.box(ax, 5.3, 0.8, 4.5, 1.8, "synthetic check:\n227 of 400 dates wrong", role="data", fs=10)
save(fig, 1, kind="diagram")
