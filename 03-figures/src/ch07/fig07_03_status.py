"""Figure 7.3: share of expected answers contradicted, by the claim status written next to them."""
from _common import S, plt, save, quiet
with quiet():
    import caldwell_bank as cb
r = cb.build().reconcile()
order = ["vendor position", "proposed design", "reconstructed from supplied artifact", "direct customer fact"]
short = ["vendor\nposition", "proposed\ndesign", "reconstructed", "direct\nfact"]
roles = ["blocker", "model", "data", "system"]
fig, ax = S.figure(3.8)
for i, (s, r_) in enumerate(zip(order, roles)):
    a, c = r.by_status[s]
    ax.bar(i, 100 * c / a, color=S.ROLE[r_], hatch=S.HATCH[r_], edgecolor="white", width=0.6)
    ax.text(i, 100 * c / a + 2, f"{c} of {a}", ha="center", fontsize=9)
ax.set_xticks(range(4)); ax.set_xticklabels(short, fontsize=9)
ax.set_ylabel("contradicted on day 24 (%)"); ax.set_ylim(0, 80)
save(fig, 3)
