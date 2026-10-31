"""Figure 34.8: services net by delivery hours for the three contract forms in the book."""
from _common import S, save
from fieldkit.contract import services_net
fig, ax = S.figure(height=4.8)
hs = list(range(0, 4201, 50))
for lab, f, role, ls in [(r"Caldwell, fixed \$200,000", lambda h: services_net(h, 150, "fixed", fee=200_000), "model", "-"),
                         (r"Pennant, fixed \$120,000", lambda h: services_net(h, 150, "fixed", fee=120_000), "data", "--"),
                         (r"Greystone, T&M \$260 to a \$450,000 cap",
                          lambda h: services_net(h, 150, "tm", bill_rate=260, cap=450_000), "system", "-")]:
    ax.plot(hs, [f(h) / 1000 for h in hs], color=S.ROLE[role], lw=1.5 if ls == "-" else 1.5, ls=ls, label=lab)
ax.axhline(0, color=S.PAL["ink"], lw=0.75)
ax.axvline(1731, color=S.PAL["grey"], lw=0.75, ls=":"); ax.text(1760, 230, "cap reached\n1,731 h", fontsize=9.5)
ax.set_xlabel("delivery hours"); ax.set_ylabel("services net ($ thousands)")
ax.legend(fontsize=9.5, loc="lower left"); ax.spines[["top", "right"]].set_visible(False)
save(fig, 8, data="04-code/ch34/output/pricing.txt (curves recomputed with fieldkit.contract)")
