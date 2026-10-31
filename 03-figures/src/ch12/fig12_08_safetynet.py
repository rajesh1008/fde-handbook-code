"""Figure 12.8: the one-page safety net, each region sized by the lines it holds (safety_net_run.py)."""
from _common import S, plt, save, blank
from fieldkit.bid import extract
from harbourline import RESPONSE_V10, standards, NOT_PROMISED
c = extract(RESPONSE_V10)
regions = [("numbers we defend", sum(x.kind == "commitment" and x.has_number for x in c), "cost"),
           ("estate, sourced to Harbourline", sum(x.kind == "estate" for x in c), "data"),
           ("Harbourline decides", sum(x.status == "D" for x in c), "approval"),
           ("deviations requested", sum(s.outcome == "deviation requested" for s in standards()), "blocker"),
           ("not promised", len(NOT_PROMISED), "evidence"), ("boundary sentence", 1, "model")]
fig, ax = S.figure(4.4); blank(ax, (0, 10), (0, 30))
y = 29.8
for name, n, role in regions:
    h = n * 0.95 + 0.8
    y -= h
    S.box(ax, 2.0, y, 6.0, h - 0.2, f"{name}: {n}", role=role, fs=10)
save(fig, 8, kind="diagram")
