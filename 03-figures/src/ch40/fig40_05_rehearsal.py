"""Figure 40.5: the day-177 reconstruction rehearsal, 40 v0 decisions, element by element."""
from _common import S, save, text, nums
rows = [l for l in text("rehearse_v0").splitlines()[2:10]]
names = [l[:23].strip() for l in rows]; vals = [nums(l[23:]) for l in rows]
assert names[3] == "prompt and model" and vals[3][2:4] == [18, 22]
cols = [("verified", "approval", 0), ("inferred", "evidence", 2), ("contradicted", "blocker", 3), ("not applicable", "light", 5)]
fig, ax = S.figure(height=4.4)
for i, v in enumerate(vals):
    left = 0
    for lab, role, k in cols:
        c = S.PAL["light"] if role == "light" else S.ROLE[role]
        ax.barh(i, v[k], 0.6, left=left, color=c, label=lab if i == 3 or (role == "light" and i == 6) or (role == "approval" and i == 0) else None)
        left += v[k]
ax.set_yticks(range(8)); ax.set_yticklabels(names); ax.invert_yaxis(); ax.set_xlim(0, 40)
ax.set_xlabel("decisions in the rehearsal sample (40)")
pass
h, l = ax.get_legend_handles_labels(); d = dict(zip(l, h))
ax.legend([d[k] for k in ("verified", "inferred", "contradicted", "not applicable")], ["verified", "inferred", "contradicted", "not applicable"],
          fontsize=9, loc="lower center", bbox_to_anchor=(0.45, -0.38), ncol=4)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch40/output/rehearse_v0.txt")
