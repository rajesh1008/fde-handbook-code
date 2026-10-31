"""Figure 35.6: fields the drafting service read, against the seven the task needs (minimum necessary)."""
from _common import S, save, text, nums
lines = [l for l in text("minimum").splitlines() if "fields read" in l]
v1, v2 = nums(lines[0].split("fields read")[1]), nums(lines[1].split("fields read")[1])
assert v1[:3] == [16, 7, 9] and v2[2] == 0
fig, ax = S.figure(height=3.9)
for i, (lab, v) in enumerate((("v1: whole packet", v1), ("v2: allowlist", v2))):
    ax.barh(i, v[1], 0.5, color=S.ROLE["system"], label="needed by the task" if i == 0 else None)
    ax.barh(i, v[2], 0.5, left=v[1], color=S.ROLE["blocker"], label="read beyond need" if i == 0 else None)
    ax.text(v[0] + 0.3, i, f"{v[0]:.0f} read, {v[2]:.0f} beyond need", va="center", fontsize=9.5)
ax.set_yticks([0, 1]); ax.set_yticklabels(["v1: whole packet", "v2: allowlist"]); ax.invert_yaxis()
ax.set_xlim(0, 24); ax.set_xlabel("referral packet fields read per call")
ax.legend(fontsize=9.5, loc="lower right"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 6, data="04-code/ch35/output/minimum.txt")
