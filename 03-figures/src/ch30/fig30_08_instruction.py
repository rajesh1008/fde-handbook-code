"""Figure 30.8: the day-146 supplement ruling, one prompt line vs relabel and retrain (Listing 30.5)."""
from _common import S, save, text, nums
t = text("instructions").splitlines()
pr = nums([l for l in t if "supplement test set" in l][0])[1]
rows = [nums(l) for l in t if l.strip()[:1].isdigit()]
fig, ax = S.figure(height=3.9)
k = [r[0] for r in rows]; y = [100 * r[1] / 80 for r in rows]
ax.plot(range(len(k)), y, color=S.ROLE["system"], lw=S.LW["emphasis"], marker="o")
ax.axhline(100 * pr / 80, color=S.ROLE["model"], lw=S.LW["control"])
for i, r in enumerate(rows):
    S.label(ax, i, y[i] + 4, f"{int(r[1])}/80", ha="center", fs=9)
ax.set_xticks(range(len(k)), [str(int(v)) for v in k], fontsize=9)
ax.set_xlabel("relabeled supplement examples in the retrain"); ax.set_ylabel("supplements filed as none (%)")
ax.set_ylim(0, 112)
S.label(ax, 0, 100 * pr / 80 + 3, f"prompted: one added line, {int(pr)}/80", color=S.ROLE["model"], fs=9)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 8, data="04-code/ch30/output/instructions.txt")
