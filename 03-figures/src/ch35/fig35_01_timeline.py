"""Figure 35.1: Greystone, data-protection pass on day 98 to the approved data map v2 on day 129 (ledger ch35)."""
from _common import S, save, blank
fig, ax = S.figure(height=4.9); blank(ax, (94, 134), (0, 10))
ax.plot([96, 132], [5, 5], color=S.PAL["grey"], lw=1.5)
ev = [(98, 98.5, "drawn map\napproved", "approval", 1), (117, 110.5, "sandbox\nweek", "data", 1),
      (122, 119.5, "generator:\n5 findings", "blocker", 1), (129, 127.5, "map v2\nsigned", "approval", 1),
      (122, 104, "scan: 187 of\n600 entries", "blocker", -1), (124, 115.5, "rescan\nclean", "evidence", -1),
      (128, 124.5, "digest\nrerun", "system", -1), (131, 130.5, "pilot", "model", -1)]
for d, cx, t, r, side in ev:
    y = 6.2 if side > 0 else 1.3
    ax.plot([d, cx], [5, y if side > 0 else y + 2.4], color=S.PAL["grey"], lw=0.75)
    S.box(ax, cx - 2.6, y, 5.2, 2.4, t, role=r, fs=9.5)
    ax.plot(d, 5, "o", color=S.ROLE[r], ms=6)
for d in range(95, 135, 5):
    ax.text(d, 4.2, f"{d}", ha="center", fontsize=9, color=S.PAL["ink"])
ax.text(95, 3.4, "day", ha="left", fontsize=9)
save(fig, 1, kind="diagram", data="04-code/ch35/output/datamap_v1.txt, scan_before.txt, scan_after.txt, datamap_v2.txt")
