"""Figure 23.6: the four versions of CM-WL-07 in one folder and what the lifecycle register made of them
(supersession.txt; dates from caldwell_docs.WL)."""
from _common import S, save
import caldwell_docs as C
fig, ax = S.figure(height=3.9)
y = {"1": 3, "2": 2, "3": 1, "4": 0}
role = {"1": "evidence", "2": "blocker", "3": "approval", "4": "data"}
yr = lambda d: d // 10000 + ((d // 100) % 100 - 1) / 12
ends = {"1": yr(20220601), "2": yr(20240901), "3": 2027.0, "4": 2027.0}
tag = {"1": "superseded", "2": "superseded", "3": "current, V-118", "4": "draft, not approved"}
for v, eff, _ in C.WL:
    ax.barh(y[v], ends[v] - yr(eff), left=yr(eff), color=S.ROLE[role[v]], height=0.5)
    ax.text(yr(eff) + 0.08, y[v] + 0.36, f"v{v} {tag[v]}", fontsize=9.5, color=S.PAL["ink"])
ax.axvline(yr(20260515), color=S.PAL["ink"], lw=1.0, ls="--")
ax.text(yr(20260515) - 0.08, 3.62, "live claim", fontsize=9.5, ha="right", color=S.PAL["ink"])
ax.set_yticks([]); ax.set_xlim(2019, 2027); ax.set_ylim(-0.5, 3.9); ax.set_xlabel("effective from (year)")
ax.spines[["top", "right", "left"]].set_visible(False)
save(fig, 6, data="04-code/ch23/caldwell_docs.py (WL) and output/supersession.txt")
