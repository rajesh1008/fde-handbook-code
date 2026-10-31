"""Figure 23.5: searches that would show a moved file to a non-litigation user, by ACL sync cadence (acl_drift.txt)."""
from _common import S, save, text, nums
rows = []
for l in text("acl_drift").splitlines():
    for k, lab in (("weekly", "weekly"), ("nightly", "nightly"), ("hourly", "hourly"), ("ACL checked", "at query time")):
        if l.startswith(k) and "applied" not in l:
            h, n = nums(l)[-2:]; rows.append((lab, h, n))
fig, ax = S.figure(height=3.9)
for i, (lab, h, n) in enumerate(rows):
    ax.barh(3 - i, n, color=S.ROLE["blocker"] if n else S.ROLE["approval"], height=0.55)
    ax.text(n + 1.2, 3 - i, f"{int(n)} searches, {int(h)} h open", va="center", fontsize=10, color=S.PAL["ink"])
ax.set_yticks([3, 2, 1, 0], [r[0] for r in rows]); ax.set_xlim(0, 95)
ax.set_xlabel("exposed searches after the day 90 move (of 721)"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch23/output/acl_drift.txt")
