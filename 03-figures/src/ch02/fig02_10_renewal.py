"""Figure 2.10: renewal band by months to production, with the three field estimates placed on it."""
from _common import S, save, title, SHORT, FIGSIZE
import matplotlib.pyplot as plt
from contracts import CONTRACTS, FIELD_ESTIMATE
from margin import renewal_probability

xs = [x / 10 for x in range(10, 141)]
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.step(xs, [renewal_probability(x) * 100 for x in xs], where="post", color=S.ROLE["evidence"], lw=2.2)
ax.axhline(20, color=S.ROLE["blocker"], ls=":", lw=1.3); ax.text(13.9, 22, "never live: 20%", ha="right", fontsize=9, color=S.PAL["ink"])
ax.axhline(90, color=S.ROLE["approval"], ls="--", lw=1.2); ax.text(13.9, 86, "target above 90%", ha="right", fontsize=9, color=S.PAL["ink"])
for (k, mk), dy in zip([("caldwell", "o"), ("greystone", "s"), ("pennant", "D")], (-9, -9, 5)):
    m = FIELD_ESTIMATE[k].months_to_production
    r = renewal_probability(m) * 100
    ax.plot(m, r, mk, color=S.ROLE["cost"], ms=9); ax.annotate(SHORT[k], (m, r), (m + (0.3 if k == "caldwell" else -0.2), r + dy), fontsize=9, ha="left" if k == "caldwell" else "right")
ax.set_xlabel("months from signature to production"); ax.set_ylabel("renewal probability, %")
ax.set_ylim(0, 100); ax.set_xlim(1, 14)
title(ax, "Northlight renewal bands (illustrative): the cliff sits at months 6 and 9")
save(fig, 10)
