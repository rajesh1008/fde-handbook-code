"""Sprint acceptance and production approval: different owner, evidence and scope."""
from _common import S, save, blank
fig, ax = blank(3.9)
S.label(ax, 3, 90, "sprint acceptance", fs=11)
S.label(ax, 59, 90, "production approval", fs=11)
for i, (a, b) in enumerate([("item owner", "gate owner"), ("item criteria", "evidence pack"),
                            ("one increment", "whole system"), ("every two weeks", "once per release")]):
    y = 66 - i * 19
    S.box(ax, 3, y, 36, 14, a, role="evidence", fs=10)
    S.box(ax, 59, y, 38, 14, b, role="approval", fs=10)
S.label(ax, 49, 50, "not\nequal", fs=10, ha="center")
save(fig, 12, kind="diagram")
