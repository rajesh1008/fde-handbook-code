"""Figure 25.1: five release levels, each approved separately; Caldwell and Greystone on day 113."""
from _common import S, save, blank
fig, ax = S.figure(height=4.6)
blank(ax, (0, 10), (0, 6.4))
levels = ["read", "draft", "write", "background", "memory"]
cal = [("granted", "approval"), ("granted", "approval"), ("preprod only", "data"), ("not granted", None), ("not granted", None)]
gre = [("sandbox", "approval"), ("sandbox", "approval"), ("refused", "blocker"), ("not granted", None), ("not granted", None)]
S.label(ax, 4.6, 6.05, "Caldwell", fs=10.5, ha="center", weight="bold")
S.label(ax, 8.0, 6.05, "Greystone", fs=10.5, ha="center", weight="bold")
for i, lv in enumerate(levels):
    y = 4.9 - i * 1.15
    S.box(ax, 0.2, y, 2.6, 0.85, lv, role="evidence", fs=10)
    for x, (t, role) in ((3.3, cal[i]), (6.7, gre[i])):
        if role:
            S.box(ax, x, y, 2.6, 0.85, t, role=role, fs=10)
        else:
            S.box(ax, x, y, 2.6, 0.85, t, role="evidence", fs=10, ls="--", hatch=False)
save(fig, 2, kind="diagram", data="04-code/ch25/output/boundaries.txt")
