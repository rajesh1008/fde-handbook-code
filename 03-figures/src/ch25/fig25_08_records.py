"""Figure 25.8: three records written by three parties at three times, joined by keys, never overwritten."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6))
items = [("recommendation", "agent, day d", "model"), ("human response", "adjuster, day d", "approval"),
         ("final outcome", "extract, day d+1", "system")]
for i, (h, who, role) in enumerate(items):
    x = 0.2 + i * 3.3
    S.box(ax, x, 3.4, 2.9, 1.4, f"{h}\n{who}", role=role, fs=10)
S.arrow(ax, 3.1, 4.1, 3.5, 4.1); S.arrow(ax, 6.4, 4.1, 6.8, 4.1)
S.label(ax, 3.3, 4.6, "rec_id", fs=9.5, ha="center", family="JetBrains Mono")
S.label(ax, 6.6, 4.6, "case", fs=9.5, ha="center", family="JetBrains Mono")
S.box(ax, 2.0, 0.6, 6.0, 1.3, "join: accepted, edited, rejected\nagainst what happened", role="evidence", fs=10)
for x in (1.65, 4.95, 8.25):
    S.arrow(ax, x, 3.4, 5.0, 1.9, ls="--", weight="data")
save(fig, 8, kind="diagram", data="04-code/fieldkit/fieldkit/actions.py")
