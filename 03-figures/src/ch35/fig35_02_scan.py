"""Figure 35.2: entries with personal data in the provider's stored-request export, by scan method and sample size."""
from _common import S, save, text, nums
rows = [nums(l) for l in text("tryit_b").splitlines()]
n = [r[0] for r in rows]; pat = [r[1] for r in rows]; full = [r[2] for r in rows]
assert full[-1] == 187 and pat[-1] == 95
fig, ax = S.figure(height=4.4)
x = range(len(n))
ax.bar([i - 0.2 for i in x], pat, 0.38, color=S.ROLE["evidence"], label="patterns only")
ax.bar([i + 0.2 for i in x], full, 0.38, color=S.ROLE["blocker"], label="patterns plus known values")
for i in x:
    ax.text(i - 0.2, pat[i] + 3, f"{pat[i]:.0f}", ha="center", fontsize=9.5)
    ax.text(i + 0.2, full[i] + 3, f"{full[i]:.0f}", ha="center", fontsize=9.5)
ax.set_xticks(list(x)); ax.set_xticklabels([f"{v:.0f} referrals\n({3 * v:.0f} entries)" for v in n])
ax.set_ylabel("entries holding PHI"); ax.set_ylim(0, 215)
ax.legend(fontsize=9.5, loc="upper left"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 2, data="04-code/ch35/output/tryit_b.txt, scan_before.txt")
