"""Figure 42.3: re-calibration on 600 scored production documents: the wrong-rate upper bound by threshold
against the 1.5% line; the lowest threshold under the line is 0.78 (output/replay_v1.txt)."""
import random
from _common import S, save, plt
import sys; sys.path.insert(0, str(__import__("_common").R / "04-code/ch42"))
from world import day_docs
from fieldkit.evals import wilson
r = random.Random(77)
pool = [x for x in sum((day_docs(k, fixed=True) for k in range(26, 33)), [])]
sample = [(x[2], x[3]) for x in r.sample(pool, 600)]
ts = [round(0.70 + 0.01 * i, 2) for i in range(21)]
up, share = [], []
for t in ts:
    pr = [c for c in sample if c[0] >= t]
    up.append(100 * wilson(sum(1 for c in pr if not c[1]), len(pr))[1]); share.append(100 * len(pr) / 600)
fig, ax = S.figure(height=4.4)
ax.plot(ts, up, color=S.ROLE["blocker"], lw=S.LW["emphasis"], marker="o", ms=3, label="wrong-rate upper bound")
ax.axhline(1.5, color=S.PAL["ink"], ls="--", lw=S.LW["control"]); ax.text(0.86, 1.65, "line 1.5%", fontsize=9)
ax.axvline(0.78, color=S.ROLE["approval"], lw=S.LW["control"]); ax.text(0.765, 2.62, "0.78 signed", fontsize=9, ha="right")
ax.axvline(0.80, color=S.PAL["grey"], lw=S.LW["data"], ls=":"); ax.text(0.805, 2.62, "0.80 shadow", fontsize=9)
ax.set_xlabel("proceed threshold"); ax.set_ylabel("upper bound, %")
b = ax.twinx(); b.plot(ts, share, color=S.ROLE["system"], lw=S.LW["control"], label="share proceeding")
b.set_ylabel("proceeding, %")
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = b.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, fontsize=9, loc="upper right", bbox_to_anchor=(1.0, 0.86))
save(fig, 3, kind="plot", data="04-code/ch42 world.day_docs days 26-32, seed 77, fieldkit.evals.wilson")
