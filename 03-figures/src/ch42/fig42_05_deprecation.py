"""Figure 42.5: the deprecation calendar against the change freeze, v0 and v1 (output/deprecation_v*.txt)."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4); blank(ax, (38, 80), (0, 8))
ax.axvspan(45, 75.9, ymin=0.05, ymax=0.85, color=S._mix(S.ROLE["cost"], 0.15), lw=0); ax.text(60, 6.4, "peak-season freeze", ha="center", fontsize=9.5)
for d, t in ((41, "notice"), (62, "retire")):
    ax.axvline(d, color=S.PAL["ink"], lw=S.LW["control"], ls="--"); ax.text(d, 7.5, t, ha="center", fontsize=9.5)
ax.text(38.3, 5.2, "v0", fontsize=10, weight="bold"); ax.text(38.3, 2.0, "v1", fontsize=10, weight="bold")
S.box(ax, 41, 4.6, 11, 1.3, "unread", role="blocker", fs=9.5)
S.box(ax, 62, 4.6, 14.9, 1.3, "EU lane to clerks", role="blocker", fs=9.5)
S.box(ax, 48, 1.4, 5, 1.3, "gate", role="evidence", fs=9.5)
S.box(ax, 54, 1.4, 1.9, 1.3, "", role="approval", fs=9.5)
S.box(ax, 55, 1.4, 7, 1.3, "rollback window", role="system", fs=9.5)
ax.text(54.9, 0.8, "approve, migrate", ha="center", fontsize=9)
for d in range(40, 81, 10):
    ax.text(d, 0.15, f"{d}", ha="center", fontsize=9)
save(fig, 5, kind="diagram", data="04-code/ch42/output/deprecation_v0.txt, deprecation_v1.txt")
