"""Figure 42.2: the leading signal (daily fingerprint PSI, v1) against the lagging one (silently wrong documents
per week, v0 and v1)."""
import json
from _common import S, save, text, weeks, plt
daily = json.loads(text("replay_daily.json").split("DAILY ", 1)[1])
fig, (a1, a2) = S.figure(height=5.4, nrows=2)

d = [r[0] for r in daily if r[0] <= 49]; p = [r[1] for r in daily if r[0] <= 49]
a1.plot(d, p, color=S.ROLE["data"], lw=S.LW["emphasis"])
a1.axhline(0.10, color=S.ROLE["blocker"], lw=S.LW["control"], ls="--")
a1.text(1, 0.16, "alarm 0.10", fontsize=9, color=S.PAL["ink"])
a1.axvline(19, color=S.PAL["grey"], lw=S.LW["data"]); a1.text(19.6, 0.75, "layout v2, day 19", fontsize=9)
a1.set_ylabel("fingerprint PSI"); a1.set_xlabel("production day")
w0, w1 = weeks("replay_v0"), weeks("replay_v1")
x = [r["week"] for r in w0]
a2.bar([i - 0.2 for i in x], [r["silent_all"] for r in w0], 0.4, color=S.ROLE["blocker"], label="v0: monthly sample")
a2.bar([i + 0.2 for i in x], [r["silent_all"] for r in w1], 0.4, color=S.ROLE["approval"], label="v1: leading and weekly")
a2.set_ylabel("silently wrong"); a2.set_xlabel("week"); a2.legend(fontsize=9, loc="upper right")

save(fig, 2, kind="plot", data="04-code/ch42/output/replay_daily.json.txt, replay_v0.txt, replay_v1.txt")
