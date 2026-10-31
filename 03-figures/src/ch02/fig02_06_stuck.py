"""Figure 2.6: year one flatters a stuck pilot; two-year renewal-weighted gross profit does not."""
from _common import S, save, title, SHORT, FIGSIZE
import matplotlib.pyplot as plt
from contracts import CONTRACTS, FIELD_ESTIMATE
from margin import year_one, two_year_gross_profit, with_

fig, (a, b) = plt.subplots(2, 1, figsize=(S.WIDTH_IN, 6.6))
for i, k in enumerate(CONTRACTS):
    c, p = CONTRACTS[k], FIELD_ESTIMATE[k]; s = with_(p, never_live=True)
    for j, (pl, role, lab) in enumerate([(p, "approval", "goes live"), (s, "blocker", "never live")]):
        x = i + (j - 0.5) * 0.36
        a.bar(x, year_one(c, pl).margin * 100, width=0.34, color=S.ROLE[role], hatch=S.HATCH[role] or "", edgecolor="white", label=lab if i == 0 else None)
        b.bar(x, two_year_gross_profit(c, pl)["total"] / 1e3, width=0.34, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white")
for ax in (a, b):
    ax.set_xticks(range(3)); ax.set_xticklabels([SHORT[k].split()[0] for k in CONTRACTS]); ax.axhline(0, color=S.PAL["ink"], lw=0.8)
a.set_ylabel("year-one gross margin, %"); b.set_ylabel("two-year gross profit, renewal-weighted, $k")
a.legend(frameon=False, fontsize=9, loc="lower left")
a.set_title("Year one: the stuck pilot looks better", loc="left", fontsize=10)
b.set_title("Two years: it is worth far less", loc="left", fontsize=10)

save(fig, 6)
