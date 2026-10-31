"""Figure 14.1: the five days on site, each with a room and an output; questions answered by evening."""
from _common import S, save, plt
import question_bank as qb

days = [15, 16, 17, 18, 19]
rooms = ["Mon 15\nMichael's room\n+ the floor", "Tue 16\nSam's room", "Wed 17\nthe pipeline", "Thu 18\nscoping\ndocument",
         "Fri 19\nread-back\n+ signature"]
t = [qb.tally(qb.BANK, d) for d in days]
fig, ax = S.figure(4.0)
ans = [x["answered"] for x in t]; blk = [x["blocking_open"] for x in t]
ax.bar(range(5), ans, width=0.55, color=S.ROLE["system"], hatch=S.HATCH["system"], edgecolor="white")
ax.plot(range(5), blk, color=S.ROLE["blocker"], lw=S.LW["emphasis"], marker="o")
for i, (a, b) in enumerate(zip(ans, blk)):
    ax.text(i, a + 0.8, str(a), ha="center", fontsize=10)
    ax.text(i + 0.12, b + 1.0, str(b), ha="left", fontsize=10, color=S.PAL["ink"])
ax.set_xticks(range(5)); ax.set_xticklabels(rooms, fontsize=9)
ax.set_ylim(0, 38); ax.set_ylabel("questions (bank of 34)")
h1 = plt.Rectangle((0, 0), 1, 1, fc=S.ROLE["system"], hatch=S.HATCH["system"], ec="white")
h2 = plt.Line2D([0], [0], color=S.ROLE["blocker"], lw=S.LW["emphasis"], marker="o")
ax.legend([h1, h2], ["answered by evening", "blocking questions still open"], loc="upper left", fontsize=9.5,
          frameon=False)
ax.annotate("fax path found 09:40", xy=(3.75, 31), xytext=(2.3, 35.5), fontsize=9.5,
            arrowprops=dict(arrowstyle="-|>", mutation_scale=10, color=S.PAL["ink"], lw=1))
save(fig, 1)
