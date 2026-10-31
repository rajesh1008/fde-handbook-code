"""Figure 23.9: recall at ten by question category, hybrid with identifier routing (evaluate.txt)."""
import re
from _common import S, save, text
rows = re.findall(r"^  (.+?)\s+n=\s*(\d+)\s+([\d.]+)", text("evaluate"), re.M)
fig, ax = S.figure(height=3.9)
for i, (c, n, r) in enumerate(sorted(rows, key=lambda x: float(x[2]))):
    r = float(r); ax.barh(i, r, color=S.ROLE["blocker"] if r < 0.8 else S.ROLE["evidence"], height=0.55)
    ax.text(r + 0.01, i, f"{r:.2f} (n={n})", va="center", fontsize=10, color=S.PAL["ink"])
ax.set_yticks(range(len(rows)), [c for c, *_ in sorted(rows, key=lambda x: float(x[2]))])
ax.axvline(0.86, color=S.PAL["ink"], lw=1.0, ls="--"); ax.text(0.865, 3.45, "overall 0.86", fontsize=9.5, color=S.PAL["ink"])
ax.set_xlim(0.4, 1.12); ax.set_xlabel("recall at ten, Anne's set"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 9, data="04-code/ch23/output/evaluate.txt")
