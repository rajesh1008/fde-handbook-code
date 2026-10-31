"""Figure 36.11: how the twenty attacks failed, by rule suite and prompt. A prompt alone moves the action count to zero."""
from _common import S, save, text, nums
rows = {}
for l in text("tryit-b").splitlines():
    k = l.split(":")[0].replace(" rules, prompt ", " ").strip()
    n = nums(l.split(":", 1)[1]); rows[k] = dict(zip(["reached", "blocked", "refused", "ignored", "esc"], n))
order = ["v2 plain", "v2 spotlight", "v3 plain", "v3 spotlight"]
assert rows["v2 spotlight"]["esc"] == 0 and rows["v3 plain"]["reached"] == 1
fig, ax = S.figure(height=4.4)
bottom = [0] * 4
for oc, r in (("reached", "blocker"), ("blocked", "approval"), ("refused", "model"), ("ignored", "evidence")):
    v = [rows[k][oc] for k in order]
    ax.bar(range(4), v, 0.6, bottom=bottom, color=S.ROLE[r], label=oc, edgecolor="white")
    bottom = [a + b for a, b in zip(bottom, v)]
for i, k in enumerate(order):
    ax.text(i, 20.6, f"{rows[k]['esc']:.0f} action\nescapes", ha="center", fontsize=9.5)
ax.set_xticks(range(4)); ax.set_xticklabels(["v2 rules\nplain prompt", "v2 rules\nspotlight", "v3 rules\nplain prompt", "v3 rules\nspotlight"])
ax.set_ylim(0, 24); ax.set_ylabel("attacks")
ax.legend(fontsize=9.5, loc="upper center", ncol=4, bbox_to_anchor=(0.5, -0.2))
ax.spines[["top", "right"]].set_visible(False)
save(fig, 12, data="04-code/ch36/output/tryit-b.txt")
