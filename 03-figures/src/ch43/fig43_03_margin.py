"""Figure 43.3: Northlight's margin on the operations line and the FDE share it consumes, year one. Data: model_*.txt."""
import re
from _common import S, save, text
rows = []
for which, keys in (("pennant", ("hybrid", "managed-v0", "managed")), ("caldwell", ("hybrid", "managed"))):
    t = text(f"model_{which}")
    for blk in t.split("\n\n")[1:]:
        name = blk.strip().splitlines()[0]
        m = re.search(r"\n\s+1\s+\$\s*[\d,]+\s+\$\s*[\d,]+\s+\$\s*[\d,]+\s+\$\s*[\d,]+\s+([\d.]+)%\s+([\d.]+)", blk)
        if m:
            rows.append((which, name.split(":")[0], float(m.group(1)), float(m.group(2))))
labels = [f"{w[:4]}. {n}" for w, n, *_ in rows]
fig, (a1, a2) = S.figure(height=4.2, ncols=2)
y = range(len(rows))
a1.barh(list(y), [r[2] for r in rows], color=[S.ROLE["cost"] if "managed" in r[1] else S.ROLE["system"] for r in rows],
        hatch="--")
a1.axvline(60, color=S.ROLE["approval"], lw=S.LW["control"], ls="--"); a1.axvline(40, color=S.ROLE["blocker"], lw=S.LW["control"], ls=":")
a1.set_yticks(list(y)); a1.set_yticklabels(labels, fontsize=9); a1.invert_yaxis(); a1.set_xlabel("margin, %")
a1.text(61, len(rows) - 0.6, "target", fontsize=9); a1.text(41, len(rows) - 0.6, "floor", fontsize=9)
a2.barh(list(y), [r[3] for r in rows], color=S.ROLE["evidence"], hatch="xx"); a2.set_yticks(list(y)); a2.set_yticklabels([])
a2.invert_yaxis(); a2.set_xlabel("FDE share")
save(fig, 3, data="04-code/ch43/output/model_pennant.txt, model_caldwell.txt (year 1 rows)")
