"""Figure 16.15: one number, three sources, days 44 to 58 (field accuracy, stand-in pipeline)."""
from _common import S, save
fig, ax = S.figure(height=3.9)
pts = [(44, 94.1, "v1 on synthetic v1", "data", "o"), (52, 70.7, "v1 on the real 200", "cost", "s"),
       (58, 70.8, "v1 on synthetic v2", "evidence", "^"), (58.6, 86.6, "v2 on the real 200\n(development)", "system", "D")]
for d, a, lab, role, mk in pts:
    ax.plot(d, a, mk, color=S.ROLE[role], ms=8, mec=S.PAL["ink"], mew=0.75)
    ax.text(d - 0.5, a + 1.6, f"{a:.1f}  {lab}", fontsize=9, ha="right" if d > 50 else "left", va="bottom")
ax.plot([44, 52], [94.1, 70.7], color=S.PAL["grey"], lw=S.LW["data"], ls="--")
ax.set_xlim(42, 60); ax.set_ylim(60, 102); ax.set_xlabel("engagement day"); ax.set_ylabel("field accuracy (%)")
ax.set_xticks([44, 48, 52, 56, 58])
save(fig, 15, data="04-code/ch16/output/gap_line.txt, failure_no_exceptions.txt")
