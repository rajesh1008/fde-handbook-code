"""Figure 23.7: older or draft versions ranked above the current one, by treatment, 25 version-sensitive questions
(supersession.txt)."""
from _common import S, save, text, nums
rows = []
for l in text("supersession").splitlines():
    for k, lab in (("as exported", "as exported"), ("newest effective", "recency boost"), ("lifecycle register,", "lifecycle register")):
        if l.startswith(k):
            n = nums(l.split(")")[-1]); rows.append((lab, n[-4], n[-2]))
fig, ax = S.figure(height=3.9)
w = 0.36
for i, (lab, old, dr) in enumerate(rows):
    ax.bar(i - w / 2, old, w, color=S.ROLE["blocker"], label="older version above current" if i == 0 else None)
    ax.bar(i + w / 2, dr, w, color=S.ROLE["data"], label="draft above current" if i == 0 else None)
    ax.text(i - w / 2, old + 0.4, f"{int(old)}", ha="center", fontsize=10, color=S.PAL["ink"])
    ax.text(i + w / 2, dr + 0.4, f"{int(dr)}", ha="center", fontsize=10, color=S.PAL["ink"])
ax.set_xticks(range(3), [r[0] for r in rows]); ax.set_ylim(0, 20); ax.set_ylabel("questions, of 25")
ax.legend(loc="upper right", fontsize=9.5, frameon=False); ax.spines[["top", "right"]].set_visible(False)
save(fig, 7, data="04-code/ch23/output/supersession.txt")
