"""Figure 5.2: who pays for 840 integration hours in each home."""
from _common import S, save, plt, FIGSIZE
import economics as E

rows = E.integration_tax_split(E.reference_hours()[1])
names = ["product vendor\n(fixed fee)", "integrator\n(T&M)", "model lab\n+ partner"]
series = [("customer pays", lambda r: r.customer_pays, "system"),
          ("employer net", lambda r: r.employer_net, "cost"),
          ("partner net", lambda r: r.partner_net, "data")]
fig, ax = plt.subplots(figsize=FIGSIZE)
w = 0.26
for j, (lab, f, role) in enumerate(series):
    for i, r in enumerate(rows):
        v = f(r) / 1e3
        y = i + (j - 1) * w
        ax.barh(y, v, height=w * 0.95, color=S.ROLE[role], hatch=S.HATCH[role], edgecolor="white",
                label=lab if i == 0 else None)
        if v != 0:
            ax.text(v + (4 if v >= 0 else -4), y, f"{'-' if v < 0 else ''}${abs(v):,.0f}k", va="center",
                    ha="left" if v >= 0 else "right", fontsize=9)
ax.axvline(0, color=S.PAL["ink"], lw=1)
ax.set_yticks(range(3)); ax.set_yticklabels(names, fontsize=9.5); ax.invert_yaxis()
ax.set_xlim(-190, 260); ax.set_xlabel("thousands of US dollars, illustrative")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncols=3, fontsize=9, frameon=False)
save(fig, 2)
