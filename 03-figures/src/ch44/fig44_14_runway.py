"""Figure 44.14: cash over 18 months for three ways of starting independent work."""
from _common import S, save, text
L = text("portfolio").splitlines()
fig, ax = S.figure(height=4.2)
roles = ["blocker", "approval", "data"]; labs = ["thin portfolio", "portfolio of proof", "one client, then a gap"]
k = 0
for i, l in enumerate(L):
    if l.strip().endswith("k") and "53k" in l:
        v = [int(x[:-1]) for x in l.split()]
        ax.plot(range(1, 19), v, color=S.ROLE[roles[k]], lw=S.LW["emphasis"] if k == 1 else 1.5,
                ls="-" if k != 2 else "--", marker="o", ms=3, label=labs[k]); k += 1
ax.axhline(60, color=S.PAL["ink"], lw=0.75, ls=":"); ax.text(18, 63, "starting savings", fontsize=9, ha="right")
ax.set_xticks(range(1, 19, 2)); ax.set_xlabel("month since leaving"); ax.set_ylabel("cash, US$ thousands (pre-tax)")
ax.set_ylim(0, 210); ax.legend(loc="upper left", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
save(fig, 14, data="04-code/ch44/output/portfolio.txt")
