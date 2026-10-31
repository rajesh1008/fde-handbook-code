"""Figure 16.12: the custody chain the sample manifest records, one named person per link."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6))
links = [("drawn\nNatarajan", "system"), ("signed for\nKessler", "approval"), ("stored\nCaldwell AWS", "evidence"),
         ("hashed\nsha256 per file", "data"), ("deleted\nend + 90 days", "cost")]
for i, (t, role) in enumerate(links):
    x = 0.1 + i * 2.0
    S.box(ax, x, 2.4, 1.75, 1.5, t, role=role, fs=10)
    if i < 4:
        S.arrow(ax, x + 1.75, 3.15, x + 2.0, 3.15)
S.label(ax, 0.1, 1.4, "a one-space edit changes the hash", fs=10, color=S.PAL["slate"])
save(fig, 12, kind="diagram", data="04-code/ch16/output/sample_plan.txt")
