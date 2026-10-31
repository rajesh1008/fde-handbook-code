"""Figure 21.6: page legibility of the 2,000 sample documents by channel, with the 0.65 gate and the marginal band."""
import sys
from _common import S, save, R
sys.path.insert(0, str(R / "04-code/ch21"))
from pennant import feed, LEGIBLE_AT
docs = feed()
fig, ax = S.figure(height=3.9)
bins = [0.45 + 0.02 * i for i in range(29)]
scan = [d["legibility"] for d in docs if d["channel"] == "scan"]
photo = [d["legibility"] for d in docs if d["channel"] == "photo"]
ax.hist([scan, photo], bins=bins, stacked=True, color=[S.ROLE["system"], S.ROLE["data"]], label=["mailbox scan", "phone photo"])
ax.axvline(LEGIBLE_AT, color=S.ROLE["blocker"], lw=S.LW["emphasis"])
ax.axvspan(0.65, 0.75, color=S.PAL["mist"], zorder=0)
ax.text(LEGIBLE_AT - 0.005, 150, "gate 0.65", ha="right", fontsize=10, color=S.PAL["ink"])
ax.text(0.70, 175, "marginal", ha="center", fontsize=10, color=S.PAL["ink"])
ax.set_xlabel("lowest page confidence"); ax.set_ylabel("documents (EDI omitted: 1.0)")
ax.legend(loc="upper left", fontsize=10); ax.set_ylim(0, 190)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 6, data="04-code/ch21/pennant.py feed()")
