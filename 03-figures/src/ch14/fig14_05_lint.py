"""Figure 14.5: the scoping document on Thursday night (v0.3, refused) and Friday afternoon (v1.0, signed)."""
from collections import Counter
from _common import S, save, plt
import pipeline as pl, projection as pj, scoping_doc as sd
from decision_tree import CLASSES, split

v03 = sd.draft_v03()
sp = split(pl.ELECTRONIC)
inv = dict(electronic=412, fax=253, steps_e=25, steps_f=25, det_e=sp[CLASSES[0]], model_e=sp[CLASSES[2]] + sp[CLASSES[3]])
v10 = sd.signed_v10(pj.project(pl.ELECTRONIC), inv)
fig, (a1, a2) = S.figure(6.0, nrows=2, gridspec_kw=dict(height_ratios=[1.6, 1]))
c = Counter(x.split()[0].lower() for x in sd.lint(v03))
keys = sorted(c, key=lambda k: (-c[k], k))
a1.barh(range(len(keys)), [c[k] for k in keys], height=0.6, color=S.TINT["blocker"], edgecolor=S.ROLE["blocker"],
        hatch=S.HATCH["blocker"], lw=1.2)
a1.set_yticks(range(len(keys))); a1.set_yticklabels(keys, fontsize=9); a1.invert_yaxis()
a1.set_xlim(0, 3); a1.set_xticks([0, 1, 2, 3])
a1.set_xlabel(f"v0.3, Thursday night: {len(sd.lint(v03))} refusals in {len(v03)} lines")
mix = sd.status_mix(v10)
roles = ["approval", "evidence", "cost", "model", "blocker"]
names = list(mix)
vals = list(mix.values())
a2.barh(range(5), vals, height=0.6, color=[S.TINT[r] for r in roles], edgecolor=[S.ROLE[r] for r in roles], lw=1.2)
for i, v in enumerate(vals):
    a2.text(v + 0.15, i, str(v), va="center", fontsize=10)
a2.set_yticks(range(5)); a2.set_yticklabels(names, fontsize=9); a2.invert_yaxis()
a2.set_xlim(0, 9); a2.set_xlabel(f"v1.0, signed Friday: {len(v10)} lines by claim status, 0 refusals")
save(fig, 5)
