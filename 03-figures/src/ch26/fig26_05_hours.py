"""Figure 26.5: the expert-hours budget Anne Kessler approved (Listing 26.2, stand-in minutes)."""
from _common import S, save, js
d = js("goldset_build")
labels = ["calibration", "labeling", "second labels", "adjudication", "rubric meetings"]
roles = ["evidence", "data", "data", "approval", "system"]
fig, ax = S.figure(height=3.8)
for i, ((name, h), lab, r) in enumerate(zip(d["rows"], labels, roles)):
    y = len(labels) - 1 - i
    ax.barh(y, h, color=S.ROLE[r], hatch=S.HATCH[r], edgecolor="white", height=0.55)
    ax.text(h + 0.6, y, f"{h:.1f} h", va="center", fontsize=10)
ax.set_yticks(range(len(labels)), labels[::-1])
ax.set_xlim(0, 38); ax.set_xlabel(f"expert hours (total {sum(h for _, h in d['rows']):.1f})")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch26/output/goldset_build.json")
