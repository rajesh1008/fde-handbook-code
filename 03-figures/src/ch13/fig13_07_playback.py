"""Mid-sprint playback at Caldwell: two readiness measures on the first 200 real documents against their thresholds."""
from _common import S, save, plt
from playback import TRACE_FINDINGS
fig, ax = S.figure(3.9)
for y, (what, seen, need, key) in enumerate(TRACE_FINDINGS):
    ax.barh(y, seen * 100, color=S.ROLE["data"], hatch=S.HATCH["data"], edgecolor="white", height=0.5)
    ax.plot([need * 100] * 2, [y - 0.35, y + 0.35], color=S.PAL["coral"], lw=S.LW["emphasis"])
    ax.text(seen * 100 - 1, y, f"{seen:.1%}", ha="right", va="center", fontsize=10,
            bbox=dict(facecolor="white", edgecolor="none", pad=1))
    ax.text(need * 100 + 0.5, y + 0.4, f"threshold {need:.0%} ({key})", fontsize=9)
ax.set_yticks([0, 1]); ax.set_yticklabels([t[0] for t in TRACE_FINDINGS], fontsize=9)
ax.set_xlim(60, 100); ax.set_ylim(-0.6, 1.9); ax.set_xlabel("percent of the 200 documents")
ax.invert_yaxis()
save(fig, 7)
