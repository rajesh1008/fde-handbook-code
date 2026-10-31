"""Figure 30.6: monthly cost by volume for the prompted arm and three serving options (Listing 30.3)."""
from _common import S, save, text, nums
t = text("cost").splitlines()
i = [k for k, l in enumerate(t) if l.startswith("option")][0]
rows = []
for l in t[i + 1:i + 5]:
    n = nums(l[44:]); rows.append((l[:44].strip(), n[0], n[-1]))
fig, ax = S.figure(height=4.0)
cols = ["model", "system", "blocker", "data"]; lab = ["prompted", "A per-token hosting", "B self-hosted GPU", "C CPU encoder"]
for (name, a, b), c, lb in zip(rows, cols, lab):
    slope = (b - a) / 145000; x = [0, 160000]; y = [a - slope * 5000, a + slope * 155000]
    ax.plot(x, y, color=S.ROLE[c], lw=S.LW["emphasis"] if c == "system" else S.LW["control"])
    S.label(ax, 161000, y[1] + {"A per-token hosting": -45, "C CPU encoder": 45}.get(lb, 0) + {"prompted": 40, "B self-hosted GPU": -40}.get(lb, 0), lb, color=S.PAL["ink"], fs=9, va="center")
ax.axvline(14800, color=S.PAL["ink"], lw=S.LW["data"], ls=":")
S.label(ax, 16500, 1150, "Caldwell,\n14,800 a month", fs=9)
ax.set_xlim(0, 160000); ax.set_ylim(0, 2100)
ax.set_xticks([0, 50000, 100000, 150000], ["0", "50k", "100k", "150k"], fontsize=9)
ax.set_xlabel("documents per month"); ax.set_ylabel("monthly cost incl. ownership ($)")
ax.spines[["top", "right"]].set_visible(False)
ax.set_position([0.13, 0.14, 0.58, 0.8])
save(fig, 6, data="04-code/ch30/output/cost.txt")
