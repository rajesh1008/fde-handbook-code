"""Figure 4.8: the oversight profile on the seeded stand-in (oversight.py): review share needed per target."""
from _common import S, save, title
import matplotlib.pyplot as plt
from oversight import simulate, profile, SYSTEMS

targets = [0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98]
fig, ax = plt.subplots(figsize=(S.WIDTH_IN, 4.2))
styles = {"pipeline A": (S.ROLE["model"], "-", "o"), "pipeline B": (S.ROLE["cost"], "--", "s")}
for name, kw in SYSTEMS.items():
    rows = simulate(**kw)
    col, ls, mk = styles[name]
    pts = [(t, profile(rows, t)) for t in targets]
    ok = [(t * 100, p["review_share"] * 100) for t, p in pts if p["threshold"] is not None]
    ax.plot([a for a, _ in ok], [b for _, b in ok], color=col, ls=ls, lw=1.8, label=name)
    for (t, p) in pts:
        if p["threshold"] is None:
            continue
        ax.plot(t * 100, p["review_share"] * 100, marker=mk, ms=7, color=col,
                markerfacecolor=col if p["qualifies"] else "white", markeredgewidth=1.5)
    last = ok[-1]
    ax.text(last[0] + 0.15, last[1], f"{name}\nstops at {last[0]:.0f}%" if last[0] < 98 else name,
            fontsize=9, va="center")
ax.plot([], [], marker="o", ls="", color=S.PAL["ink"], markerfacecolor="white", label="fails on held-out half")
ax.set_xlim(89.5, 99.8); ax.set_ylim(0, 80)
ax.set_xlabel("reliability target on fields sent without review, %")
ax.set_ylabel("fields sent to review, %")
ax.legend(frameon=False, fontsize=9, loc="upper left")
title(ax, "Same accuracy, very different review share")
save(fig, 8, data="04-code/ch04/oversight.py seeded stand-in (400 documents x 10 fields; not Caldwell data)")
