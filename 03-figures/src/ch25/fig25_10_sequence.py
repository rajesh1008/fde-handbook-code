"""Figure 25.10: one lost response on day 109: the claim committed, the agent loop called again with a new key."""
from _common import S, save, blank
fig, ax = S.figure(height=4.6)
blank(ax, (0, 10), (0, 7))
for x, t, r in ((1.2, "agent loop", "model"), (5.0, "WriteBack", "evidence"), (8.6, "claims-core", "system")):
    S.box(ax, x - 1.0, 6.1, 2.0, 0.7, t, role=r, fs=10)
    ax.plot([x, x], [0.3, 6.1], color=S.PAL["grey"], lw=0.75, ls="--")
rows = [(1.2, 5.0, 5.4, "submit, key call-0107", None), (5.0, 8.6, 4.7, "FNOL-1, FNOL-2", None),
        (8.6, 5.0, 4.0, "claim committed, page times out", "blocker"), (5.0, 1.2, 3.3, "unknown", None),
        (1.2, 5.0, 2.4, "submit again, key call-0108", "blocker"), (5.0, 8.6, 1.7, "no key match: new claim", "blocker")]
for x1, x2, y, t, emph in rows:
    S.arrow(ax, x1, y, x2, y, weight="emphasis" if emph else "control",
            color=S.ROLE["blocker"] if emph else None)
    S.label(ax, (x1 + x2) / 2, y + 0.22, t, fs=9.5, ha="center")
save(fig, 10, kind="diagram", data="04-code/ch25/output/day109_retry.txt")
