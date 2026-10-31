"""Signature 4: the sponsor map. Five role columns (sponsor, operator, blocker, approver, owner) and a champion
network row. One template for every recurrence; only the 2.5 pt emphasis stroke moves. A chapter calls
draw(ax, columns, champions, emphasis) where columns maps role -> list of short names (empty list = nobody),
champions is a list of short names and emphasis is a set of names (or 'nobody:<role>')."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "05-build/design"))
import fde_style as S

ROLES = ["sponsor", "operator", "blocker", "approver", "owner"]
ROLE_COLOR = dict(sponsor="cost", operator="system", blocker="blocker", approver="approval", owner="evidence")


def from_map(m, short=lambda p: p.name.split()[-1]):
    cols = {r: [short(p) for p in m.holders(r)] for r in ROLES}
    return cols, [short(p) for p in m.champions()]


def draw(ax, columns, champions, emphasis=frozenset(), rows=3):
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.4); ax.axis("off")
    w, gap = 1.8, 0.2
    for i, r in enumerate(ROLES):
        x = 0.1 + i * (w + gap)
        S.box(ax, x, 5.5, w, 0.75, r, role=ROLE_COLOR[r], fs=10.5, hatch=False, lw=S.LW["control"])
        names = columns.get(r, [])
        if not names:
            lw = S.LW["emphasis"] if f"nobody:{r}" in emphasis else S.LW["data"]
            S.box(ax, x, 4.4, w, 0.85, "nobody", role=ROLE_COLOR[r], fs=10, ls="--", hatch=False, lw=lw)
        for j, n in enumerate(names[:rows]):
            y = 4.4 - j * 1.05
            lw = S.LW["emphasis"] if n in emphasis else S.LW["control"]
            S.box(ax, x, y, w, 0.85, n, role=ROLE_COLOR[r], fs=10, lw=lw)
    S.box(ax, 0.1, 0.25, 2.6, 0.85, "champion network", role="data", fs=10.5, hatch=False)
    if not champions:
        lw = S.LW["emphasis"] if "nobody:champion" in emphasis else S.LW["data"]
        S.box(ax, 3.0, 0.25, 1.8, 0.85, "nobody", role="data", fs=10, ls="--", hatch=False, lw=lw)
    for k, n in enumerate(champions):
        lw = S.LW["emphasis"] if n in emphasis else S.LW["control"]
        S.box(ax, 3.0 + k * 2.0, 0.25, 1.8, 0.85, n, role="data", fs=10, lw=lw)
    ax.plot([0.1, 9.9], [1.3, 1.3], color=S.PAL["light"], lw=S.LW["data"])
