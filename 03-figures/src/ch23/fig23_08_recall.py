"""Figure 23.8: recall at ten on the vendor's synthetic set and on Anne's 150 questions, four retrievers (evaluate.txt)."""
from _common import S, save, text, nums
rows = []
for l in text("evaluate").splitlines():
    for k, lab in (("lexical", "lexical"), ("vector", "vector"), ("hybrid, plain", "hybrid"), ("hybrid +", "hybrid +\nidentifiers")):
        if l.startswith(k):
            n = nums(l.split(")")[-1] if ")" in l else l); rows.append((lab, n[-4], n[-3]))
fig, ax = S.figure(height=3.9); w = 0.36
for i, (lab, syn, an) in enumerate(rows):
    ax.bar(i - w / 2, syn, w, color=S.PAL["grey"], label="vendor synthetic set" if i == 0 else None)
    ax.bar(i + w / 2, an, w, color=S.ROLE["approval"] if i == 3 else S.ROLE["evidence"], label="Anne's questions" if i == 0 else None)
    ax.text(i + w / 2, an + 0.015, f"{an:.2f}", ha="center", fontsize=10, color=S.PAL["ink"])
ax.set_xticks(range(4), [r[0] for r in rows]); ax.set_ylim(0.5, 1.05); ax.set_ylabel("recall at ten")
ax.legend(loc="upper left", fontsize=9.5, frameon=False, ncol=2); ax.spines[["top", "right"]].set_visible(False)
save(fig, 8, data="04-code/ch23/output/evaluate.txt")
