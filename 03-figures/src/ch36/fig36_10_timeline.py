"""Figure 36.10: from report to residual risk in 41 hours, days 127 to 129."""
from _common import S, save, text
ret = text("retest")
assert "closed with retest: 9 of 11" in ret and "11:20 F-16" in ret
ev = [(127 + 17.67 / 24, "report, 20 items", "evidence"), (127 + 18.17 / 24, "joint triage", "system"),
      (128 + 9 / 24, "suite v3 deployed", "system"), (128 + 11.33 / 24, "F-16 closure rejected", "blocker"),
      (128 + 16 / 24, "9 of 11 retested", "approval"), (129 + 10 / 24, "F-13, F-21 to risk owner", "cost")]
fig, ax = S.figure(height=4.2)
for k, (t, lab, r) in enumerate(ev):
    y = 5 - k
    ax.plot([t], [y], "s", ms=9, color=S.ROLE[r])
    ax.text(t + 0.05, y, lab, va="center", fontsize=9.5)
ax.set_ylim(-0.6, 5.8); ax.set_yticks([])
ax.set_xlim(127.0, 130.4); ax.set_xticks([127, 128, 129, 130]); ax.set_xticklabels(["day 127", "day 128", "day 129", "day 130"])
for d in (127, 128, 129, 130):
    ax.axvline(d, color=S.PAL["light"], lw=0.75)
ax.spines[["top", "right", "left"]].set_visible(False)
save(fig, 10, data="04-code/ch36/output/retest.txt, triage.txt; Greystone calendar")
