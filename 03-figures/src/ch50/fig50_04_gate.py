"""Figure 50.4: the same draft with a model-written ratio; three checks, and which one stops each injection."""
import re
from _common import S, save, text, blank
rows = [("clean draft", "clean"), ("ratio the model wrote", "model_ratio"), ("ratio with its own calculation", "model_calc"), ("currency unlabeled", "unlabeled")]
cols = ("numeric gate", "lineage check", "currency label")
fig, ax = S.figure(height=3.9); blank(ax, (0, 10), (0, 5.2))
for j, c in enumerate(cols):
    S.label(ax, 4.6 + j * 1.85, 4.75, c, fs=9.5, ha="center", weight="bold")
for i, (name, key) in enumerate(rows):
    t = text(f"draft_{key}"); y = 3.6 - i * 1.1
    S.label(ax, 0.1, y + 0.4, name, fs=9.5, va="center")
    res = [re.search(r"numeric gate: (\w+)", t), re.search(r"lineage check: (\w+)", t), re.search(r"currency lint: (\w+)", t)]
    for j, m in enumerate(res):
        ok = m and m.group(1).lower() in ("pass", "passes", "holds", "ok")
        S.box(ax, 3.75 + j * 1.85, y, 1.7, 0.8, "pass" if ok else "stops it", role="approval" if ok else "blocker",
              fs=9.5, lw=S.LW["control"] if ok else S.LW["emphasis"])
save(fig, 4, kind="diagram", data="04-code/ch50/output/draft_*.txt")
