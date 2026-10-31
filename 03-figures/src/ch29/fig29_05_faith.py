"""Figure 29.5: claims supported by their cited passage, by question type, and the checker against Joan Mercer (Listing 29.4)."""
from _common import S, save, js
d = js("faithfulness")
by = {k: v for k, v in d["by"].items() if v[0]}
j = d["joan"]
fig, (a1, a2) = S.figure(height=3.9, ncols=2, gridspec_kw=dict(width_ratios=[1.6, 1]))
names = list(by)
for i, n in enumerate(names):
    c, s = by[n]
    a1.barh(i, 100 * s / c, height=0.6, color=S.TINT["model"], edgecolor=S.ROLE["model"])
    S.label(a1, 100 * s / c - 1, i, f"{s} of {c}", ha="right", va="center", fs=9)
a1.set_yticks(range(len(names)), [n.replace("-", "-\n", 1) if len(n) > 14 else n for n in names], fontsize=9)
a1.invert_yaxis(); a1.set_xlim(80, 100); a1.set_xlabel("claims supported (%)")
vals = [j["uns"], j["caught"], j["fa"]]
a2.bar([0, 1, 2], vals, color=[S.ROLE["evidence"], S.ROLE["approval"], S.ROLE["blocker"]], width=0.6)
for i, v in enumerate(vals):
    S.label(a2, i, v + 0.15, str(v), ha="center", fs=10)
a2.set_xticks([0, 1, 2], ["Joan:\nunsupported", "checker\ncaught", "false\nalarms"], fontsize=9)
a2.set_ylim(0, 7); a2.set_ylabel(f"claims (of {j['claims']})")
for a in (a1, a2):
    a.spines[["top", "right"]].set_visible(False)
save(fig, 5, data="04-code/ch29/output/faithfulness.json")
