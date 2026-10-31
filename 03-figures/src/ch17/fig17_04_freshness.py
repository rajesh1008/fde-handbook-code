"""Figure 17.4: why the replica answers with last night's rights."""
from _common import S, save, blank
fig, ax = S.figure(height=3.7)
blank(ax, (0, 24.5), (0, 6))
ax.plot([0, 24], [2.6, 2.6], color=S.PAL["ink"], lw=S.LW["control"])
for h in (0, 6, 12, 18, 24):
    ax.plot([h, h], [2.45, 2.75], color=S.PAL["ink"], lw=S.LW["data"]); S.label(ax, h, 1.95, f"{h:02d}:00", fs=9, ha="center")
for h, lab, role, y in ((2, "02:00 replica\nview built", "data", 3.3), (11.67, "11:40 claim\nflagged litigated", "blocker", 3.3),
                        (14.08, "14:05 search\nreturns it", "system", 0.2)):
    S.box(ax, h - 2.2, y, 4.4, 1.35, lab, role=role, fs=9.5)
    S.arrow(ax, h, y if y > 2 else y + 1.35, h, 2.65 if y > 2 else 2.55, weight="data")
S.label(ax, 17.0, 0.75, "recheck asks claims-core\nat 14:05: withheld", fs=10, color=S.PAL["ink"], weight="bold")
save(fig, 4, kind="diagram", data="chapter text; 04-code/ch17/obo_recheck.py (flag times)")
