"""Figure 29.8: the 29 failures of the first weekly scenario run, day 145, by triage outcome (Listing 29.5)."""
from _common import S, save, js
d = js("scenarios")
t = d["tri"]
names = ["agent defect", "oracle defect", "broken scenario"]
vals = [t.get(n, 0) for n in names]
fig, ax = S.figure(height=3.7)
cols = [S.ROLE["model"], S.ROLE["evidence"], S.ROLE["data"]]
ax.bar(range(3), vals, color=cols, width=0.6)
for i, v in enumerate(vals):
    S.label(ax, i, v + 0.4, f"{v} of {sum(vals)}", ha="center", fs=10)
S.label(ax, 0, vals[0] / 2, f"{d['causes']} root\ncauses", ha="center", va="center", fs=9.5, color="white", bbox=dict(boxstyle="square,pad=0.2", fc=S.ROLE["model"], ec="none"))
ax.set_xticks(range(3), names, fontsize=10); ax.set_ylim(0, 26); ax.set_ylabel("failing scenarios")
ax.spines[["top", "right"]].set_visible(False)
save(fig, 8, data="04-code/ch29/output/scenarios.json")
