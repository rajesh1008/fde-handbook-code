"""Figure 47.10: days from signature to Live Stable by the order each customer adopted the playbook."""
from _common import S, save
import sys
sys.path.insert(0, str(S.ROOT / "04-code/ch47"))
from world import TTP, N17_LOST, name  # noqa: E402
fig, ax = S.figure(height=4.0)
for (pb, rows), c, m in zip(TTP.items(), (S.ROLE["model"], S.ROLE["data"]), ("o", "s")):
    xs = list(range(1, len(rows) + 1)); ys = [d for _, d in rows]
    ax.plot(xs, ys, marker=m, color=c, label=pb)
    for x, (e, d) in zip(xs, rows):
        ax.text(x + 0.08, d + 4, name(e), fontsize=9)
x17 = len(TTP["PB-1 claims intake"])
ax.bar(x17, N17_LOST, 0.3, bottom=TTP["PB-1 claims intake"][-1][1] - N17_LOST, color=S.ROLE["blocker"], hatch="\\\\",
       ec="white", label="days lost: undeclared gateway step")
ax.set_xlabel("adoption order"); ax.set_ylabel("days to Live Stable"); ax.set_xlim(0.5, 6.9); ax.set_ylim(0, 175)
ax.legend(loc="upper right", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 10, data="04-code/ch47/output/absorb_ttp.txt; world.py TTP")
