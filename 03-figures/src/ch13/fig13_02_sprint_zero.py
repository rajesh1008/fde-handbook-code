"""Sprint zero: five outputs that make sprint one plannable."""
from _common import S, save, blank
fig, ax = blank(3.9)
outs = [("named\ncounterparts", "approval"), ("access\nrequests", "blocker"), ("golden\npaths", "data"),
        ("readiness\nregister", "evidence"), ("decision\nregister", "system")]
for i, (t, role) in enumerate(outs):
    S.box(ax, 2 + i * 19.5, 58, 17, 22, t, role=role, fs=9)
    S.arrow(ax, 10.5 + i * 19.5, 57, 50, 36)
S.box(ax, 30, 12, 40, 22, "sprint one\nplannable", role="approval", fs=11)
S.label(ax, 2, 90, "days 15-28, Caldwell", fs=10)
save(fig, 2, kind="diagram")
