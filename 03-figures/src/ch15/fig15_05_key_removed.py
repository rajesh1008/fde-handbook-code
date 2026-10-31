"""Figure 15.5: readiness score for complete deliveries and for deliveries with the key column removed."""
from _common import S, save
from fieldkit.fixtures import caldwell_sample, caldwell_register
from fieldkit.histories import caldwell_fields, greystone_fields, greystone_sample
c2, g2 = caldwell_fields(), greystone_fields()
res = [("Caldwell, v1 register", caldwell_register().assess("caldwell-claims-sample", caldwell_sample())),
       ("Caldwell, v1, key removed", caldwell_register().assess("caldwell-claims-sample", caldwell_sample(drop_column="claim_id"))),
       ("Caldwell, v2 register", c2.assess("caldwell-claims-sample", caldwell_sample(), 41, 47)),
       ("Caldwell, v2, key removed", c2.assess("caldwell-claims-sample", caldwell_sample(drop_column="claim_id"), 41, 47)),
       ("Greystone day 104, key removed", g2.assess("greystone-referral-sample", greystone_sample(drop_key=True), 99, 104)),
       ("Greystone day 112, study key", g2.assess("greystone-referral-sample", greystone_sample(), 107, 112))]
fig, ax = S.figure(height=4.0)
for i, (name, r) in enumerate(res):
    y = len(res) - 1 - i
    role = "approval" if r.ready() else "blocker"
    ax.barh(y, r.score, color=S.ROLE[role] if r.ready() else S.TINT["blocker"], hatch="" if r.ready() else S.HATCH["blocker"],
            edgecolor=S.ROLE[role], lw=S.LW["data"], height=0.6)
    ax.text(r.score + 0.015, y, f"{r.score:.2f} " + ("ready" if r.ready() else "not ready"), va="center", fontsize=9.5, color=S.PAL["ink"])
ax.set_yticks(range(len(res))); ax.set_yticklabels([n for n, _ in reversed(res)], fontsize=9.5)
ax.set_xlim(0, 1.2); ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0]); ax.set_xlabel("readiness score (weighted share of checks passed)")
save(fig, 5, data="04-code/ch15 failure_key_removed.py, greystone_day112.py")
