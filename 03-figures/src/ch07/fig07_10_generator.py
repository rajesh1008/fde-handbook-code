"""Figure 7.10: discovery items served by the day-20 memory draft against the generated and edited bank."""
from _common import S, plt, save, quiet
with quiet():
    import generate_bank as g
from discovery_snapshot import PATHS, EXCEPTIONS, GAPS, NOTES
groups = [("paths", PATHS), ("exceptions", EXCEPTIONS), ("permission gaps", GAPS), ("notes", NOTES)]
fig, ax = S.figure(3.8)
for i, (n, d) in enumerate(groups):
    mem = sum(k in g.MEMORY_DRAFT_SOURCES for k in d)
    ax.barh(i - 0.18, len(d), height=0.34, color=S.ROLE["system"], hatch=S.HATCH["system"], edgecolor="white",
            label="generated bank" if i == 0 else None)
    ax.barh(i + 0.18, mem, height=0.34, color=S.ROLE["cost"], hatch=S.HATCH["cost"], edgecolor="white",
            label="memory draft" if i == 0 else None)
    ax.text(len(d) + 0.2, i - 0.18, f"{len(d)} of {len(d)}", va="center", fontsize=9)
    ax.text(mem + 0.2, i + 0.18, f"{mem} of {len(d)}", va="center", fontsize=9)
ax.set_yticks(range(4)); ax.set_yticklabels([n for n, _ in groups], fontsize=9); ax.invert_yaxis()
ax.set_xlabel("discovery items served by at least one question"); ax.set_xlim(0, 14)
ax.legend(fontsize=9, frameon=False, loc="lower right")
save(fig, 10)
