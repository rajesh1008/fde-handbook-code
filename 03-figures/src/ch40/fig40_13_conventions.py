"""Figure 40.13: one evidence model, four homes, each with its own reader and retention."""
from _common import S, save, blank, text
t = text("conventions"); assert "2,555 days" in t and "2,190 days" in t and "365 days" in t
fig, ax = S.figure(height=4.6); blank(ax, (0, 10), (0, 8))
S.box(ax, 2.6, 6.0, 4.8, 1.5, "eight elements", role="model", fs=11)
homes = [("Caldwell:\nclaim file\n2,555 days", "approval"), ("Greystone:\ncase record\n2,190 days", "approval"),
         ("Pennant:\naudit file\n365 days", "approval"), ("Harbourline:\nnot agreed", "data")]
for i, (h, r) in enumerate(homes):
    x = 0.05 + i * 2.5
    S.box(ax, x, 0.6, 2.3, 2.9, h, role=r, fs=9.5)
    S.arrow(ax, 5.0, 6.0, x + 1.15, 3.5)
save(fig, 13, kind="diagram", data="04-code/ch40/output/conventions.txt")
