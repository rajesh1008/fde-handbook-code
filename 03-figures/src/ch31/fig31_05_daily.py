"""Figure 31.5: daily agreement with keyed claims over the shadow window (shadow_run.txt)."""
from _common import S, save, text, nums
rows = [nums(l) for l in text("shadow_run").splitlines() if l[:3].isdigit() and l[3] == " "]
days = [int(r[0]) for r in rows]; share = [r[3] for r in rows]
fig, ax = S.figure(height=4.0)
x = list(range(len(days)))
ax.plot(x, share, color=S.ROLE["model"], marker="o", lw=2)
for i, s in zip(x, share):
    S.label(ax, i, s + 0.35, f"{s:.1f}", ha="center", fs=8.5)
ax.axhline(85, color=S.ROLE["blocker"], ls="--", lw=1.2); S.label(ax, 7.1, 84.4, "draft bar 85%", fs=9)
for d, t, y in ((143, "broker\ntemplate", 91.3), (150, "orientation\nfix", 91.3), (151, "router\nv1.1", 86.2)):
    i = days.index(d); ax.axvline(i, color=S.PAL["grey"], lw=1, ls=":"); S.label(ax, i + 0.08, y, t, fs=8.5)
ax.set_xticks(x, [str(d) for d in days]); ax.set_xlabel("intake day (147 and 148 closed)")
ax.set_ylabel("agree on all six fields (%)"); ax.set_ylim(83, 92.5); ax.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch31/output/shadow_run.txt")
