"""Figure 12.4: the target architecture as five contracts, one per boundary, each stating what Harbourline's
clarifications settled (harbourline.RESPONSE_V10)."""
from _common import S, plt, save, blank
fig, ax = S.figure(4.2); blank(ax, (0, 10), (0, 7))
S.box(ax, 3.6, 2.9, 2.8, 1.2, "drafting service", role="model", fs=10.5)
ends = [((0.1, 5.4), "productivity\nsuite add-in", "system", "single sign-on", (3.6, 4.1)),
        ((7.1, 5.4), "model gateway", "system", "no streaming", (6.4, 4.1)),
        ((0.1, 0.3), "document store", "data", "list every\n10 min", (3.6, 2.9)),
        ((7.1, 0.3), "origination\nsystem", "data", "read only", (6.4, 2.9)),
        ((3.6, 0.3), "bank SIEM", "evidence", "hourly", (5.0, 2.9))]
for (x, y), name, role, contract, (cx, cy) in ends:
    S.box(ax, x, y, 2.8, 1.2, name, role=role, fs=10)
    ex, ey = x + 1.4, (y if y > 3 else y + 1.2)
    S.arrow(ax, cx, cy, ex, ey)
    S.label(ax, (cx + ex) / 2 + (0.25 if ex > cx else -0.25), (cy + ey) / 2, contract, fs=9,
            ha="left" if ex >= cx else "right", va="center")
save(fig, 4, kind="diagram")
