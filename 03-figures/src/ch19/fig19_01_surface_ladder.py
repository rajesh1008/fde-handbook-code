"""Figure 19.1: the surface ladder, from the most to the least dependable way into a system."""
from _common import S, save, blank
fig, ax = S.figure(height=4.2)
blank(ax, (0, 10), (0, 8.4))
rungs = [("API", "system"), ("database view", "system"), ("nightly export", "data"), ("queue or mailbox", "data"),
         ("batch loader", "evidence"), ("screen, scripted", "blocker"), ("screen, agent", "blocker")]
for i, (t, r) in enumerate(rungs):
    y = 7.3 - i * 1.05
    S.box(ax, 0.6 + i * 0.35, y, 5.2, 0.85, t, role=r, fs=10.5)
S.arrow(ax, 8.4, 7.9, 8.4, 0.9, weight="emphasis")
S.label(ax, 8.6, 7.6, "more\ndependable", fs=10, va="top")
S.label(ax, 8.6, 1.2, "more\nwork per\nchange", fs=10)
save(fig, 1, kind="diagram", data="fieldkit.connectors.BASE (04-code/fieldkit/fieldkit/connectors.py)")
