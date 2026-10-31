"""Figure 47.11: FDE hours per engagement by layer, by cohort, as the platform and playbooks absorb work."""
from _common import S, save
import sys
sys.path.insert(0, str(S.ROOT / "04-code/ch47"))
from world import HOURS  # noqa: E402
fig, ax = S.figure(height=4.0)
labs = ["first four", "months 11 to 14", "months 15 to 18"]
bottom = [0, 0, 0]
for k, r, h in (("bespoke", "blocker", "\\\\"), ("playbook", "data", ".."), ("platform", "system", "//")):
    vals = [c[k] for c in HOURS.values()]
    ax.bar(labs, vals, 0.55, bottom=bottom, color=S.ROLE[r], hatch=h, ec="white", label=k)
    bottom = [b + v for b, v in zip(bottom, vals)]
for i, t in enumerate(bottom):
    ax.text(i, t + 40, f"{t:,}", ha="center", fontsize=9)
ax.set_ylabel("FDE hours, signature to Live Stable"); ax.set_ylim(0, 3300)
ax.legend(loc="upper right", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 11, data="04-code/ch47/output/absorb_ttp.txt; world.py HOURS")
