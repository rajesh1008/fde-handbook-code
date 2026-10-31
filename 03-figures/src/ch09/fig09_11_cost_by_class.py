"""Figure 9.11: where the pipeline's cost per document goes, by class, beside the demo agent."""
from _common import S, save, plt
demo, new, by = weighted = __import__("_common").weighted()
parts = [("frontier", "model", "frontier model"), ("small", "data", "small model"), ("det", "system", "deterministic + rules"),
         ("platform", "evidence", "platform per document")]
fig, ax = S.figure(3.9)
ax.bar(0, demo * 100, width=0.55, color=S.ROLE["cost"], hatch=S.HATCH["cost"], edgecolor="white", label="demo agent")
bottom = 0
for key, role, lab in parts:
    v = (by.get(key, 0) + (by.get("rules", 0) if key == "det" else 0)) * 100
    ax.bar(1, v, bottom=bottom, width=0.55, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white", label=lab); bottom += v
ax.text(0, demo * 100 + 0.3, f"{demo * 100:.1f}¢", ha="center", fontsize=10)
ax.text(1, bottom + 0.3, f"{new * 100:.1f}¢", ha="center", fontsize=10)
ax.text(1.36, by["frontier"] * 50, f"frontier step\n{by['frontier'] / new:.0%} of it", fontsize=9.5, va="center")
ax.set_xticks([0, 1]); ax.set_xticklabels(["demo agent", "pipeline"]); ax.set_xlim(-0.5, 2.1)
ax.set_ylabel("cents per document, volume weighted"); ax.set_ylim(0, demo * 100 * 1.2)
ax.legend(fontsize=9, frameon=False, loc="upper right")
save(fig, 11)
