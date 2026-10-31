"""Engagement manifests for the catalog linter. Deterministic stand-in: every manifest is typed from facts the
earlier chapters recorded (chapter and day in the comment); the linter reads these, not live systems.

STORIES: one snapshot per rule, the engagement as it stood on the day the anti-pattern was exposed.
INJECTED: Greystone's kickoff map (Chapter 11, day 2), which has no operator.
AUDIT: the four engagements as recorded through the latest chapter, for the Scoreboard.
"""
import _paths  # noqa: F401
from stakeholders import Person, StakeholderMap
import greystone, pennant, caldwell

CM, NL, PN = "caldwellmutual.example", "northlight.example", "pennant.example"


def snap(sid, rule, who, when, phase="shadow", **kw):
    m = dict(id=sid, rule=rule, who=who, when=when, phase=phase, domain=kw.pop("domain", CM), alert_routes=[])
    m.update(kw)
    return m


STORIES = [
    snap("S01", "R01", "Greystone (last vendor)", "Ch11, told day 11", pilot=dict(start=0, exit_rule_day=None)),
    snap("S02", "R02", "Pennant", "Ch11, day 28", smap=pennant.DAY28),
    snap("S03", "R03", "Caldwell", "Ch41, day 176", phase="handed over",
         alert_routes=["claims-oncall@" + CM, "nl-caldwell-alerts@" + NL]),
    snap("S04", "R04", "Caldwell", "Ch34, day 137",
         commitments=[dict(id="CA-01", measurer="", documents="", computation="", interval="")]),
    snap("S05", "R05", "Caldwell", "Ch9, discovery",
         steps=[("W1", "deterministic", ["join"]), ("W2", "small model", ["classify"]),
                ("W3", "frontier model", ["extract", "arithmetic"])]),
    snap("S06", "R06", "Caldwell", "Ch8, day 24", claims=[dict(id="OD-4 sentence", history=[(-34, "V", False), (24, "F", False)])]),
    snap("S07", "R07", "Caldwell", "Ch37, day 156",
         gate=dict(gate="Shadow Exit", bar=0.80, judged_on="aggregate",
                   slices={"fax first notice": (372, 500), "other classes": (1317, 1510)})),
    snap("S08", "R08", "Caldwell", "Ch26", accuracy=[dict(value="91%", scorer="Northlight", documents="Northlight")]),
    snap("S09", "R09", "Caldwell", "Ch18", adapter=dict(key_reread=False)),
    snap("S10", "R10", "Caldwell", "Ch27", thresholds=[dict(name="router.proceed", value=0.98, chosen_by=None)]),
    snap("S11", "R11", "Pennant", "Ch20", domain=PN, models=[dict(name="extract (europe-west4)", version="latest")]),
    snap("S12", "R12", "Greystone", "Ch35", flows=[dict(flow=f"F{i}", retention_known=i != 3) for i in range(1, 6)],
         map_generated=False),
    snap("S13", "R13", "Pennant", "Ch43, day 272", phase="managed service", domain=PN,
         runbooks=[dict(id=f"RB{i}", vendor_steps=2) for i in range(1, 5)]),
    snap("S14", "R14", "Caldwell", "Ch40, day 166", packs=dict(pinned=False, ok=0, n=40)),
    snap("S15", "R15", "Pennant", "Ch10, day 23", domain=PN, playbook_steps=[("P-A2", ["TMS status API"])],
         estate=["EDI 210/214", "freight-audit mailbox"]),
]

INJECTED = snap("INJ", "R02", "Greystone", "Ch11, day 2", smap=greystone.KICKOFF)

PENNANT_NOW = StakeholderMap("Pennant", 300, [
    Person("holloway", "Grant Holloway", "Executive owner", ("sponsor", "owner"), 298, source="own words"),
    Person("clerks", "Documentation clerks (14)", "Memphis documentation team", ("operator",), 297, source="observed"),
    Person("mensah", "Kofi Mensah", "Change board", ("approver",), 296, source="own words"),
    Person("compliance", "Compliance manager", "Pennant compliance", ("blocker",), 290, source="own words"),
    Person("whitaker", "Dana Whitaker", "Freight audit manager", ("owner",), 295, source="own words"),
])
HARBOURLINE_NOW = StakeholderMap("Harbourline", 171, [
    Person("okafor", "David Okafor", "Accountable executive", ("sponsor", "owner"), 170, source="own words"),
    Person("marsh", "Helen Marsh", "Head of Model Risk", ("approver",), 168, source="own words"),
    Person("shaw", "Martin Shaw", "Enterprise architect", ("approver",), 165, source="own words"),
    Person("officers", "Credit officers", "Commercial credit", ("operator",), 169, source="observed"),
])

AUDIT = {
    "Caldwell": dict(
        id="Caldwell", phase="retained duties", domain=CM,
        alert_routes=["claims-oncall@" + CM, "claims-owner@" + CM, "mrm-monitor@" + CM],
        pilot=dict(start=142, exit_rule_day=141), smap=caldwell.DAY25,
        commitments=[dict(id="CA-01 (v5)", measurer="Anne Kessler", documents="monthly sample",
                          computation="fields sent without review", interval="95% Wilson")],
        steps=[("W3", "frontier model", ["extract"]), ("C08", "deterministic", ["arithmetic"])],
        claims=[dict(id="OD-4", history=[(-34, "V", False), (26, "D", False)])],
        gate=dict(gate="Shadow Exit (rc-1)", bar=0.80, judged_on="slices",
                  slices={"fax first notice": (372, 500), "other classes": (1317, 1510)}),
        accuracy=[dict(value="gold set", scorer="customer", documents="customer")],
        adapter=dict(key_reread=True),
        thresholds=[dict(name="router.proceed", value=0.98, chosen_by="Anne Kessler")],
        models=[dict(name="extract", version="extract-2026-04")],
        flows=[dict(flow="fields to gateway", retention_known=True)], map_generated=True,
        runbooks=[dict(id="RB-03", vendor_steps=0), dict(id="RB-05", vendor_steps=0)], drill="day 183, passed",
        packs=dict(pinned=True, ok=26, n=26),
        why={"R04": "CA-01 v5 (day 149): Anne Kessler scores a monthly sample",
             "R06": "OD-4 logged as an open decision on day 26; it rises only on Anne Kessler's answer",
             "R10": "router threshold 0.98 named to Anne Kessler",
             "R11": "extract-2026-04 pinned; version printed in every report",
             "R03": "every alert route on a Caldwell address since day 177",
             "R05": "W3 extracts only; totals moved to code step C08",
             "R07": "per-class report; fax first notice excluded by name (S-1)",
             "R12": "map generated from the running system; fields, not document text",
             "R13": "runbooks executable by Caldwell; drill 2 passed day 183",
             "R14": "26 of 26 packs rebuilt at internal audit (day 214)"}),
    "Greystone": dict(
        id="Greystone", phase="live", domain="greystone.example", alert_routes=[],
        pilot=dict(start=None, exit_rule_day=None, signed_before=True), smap=greystone.DAY12,
        commitments=[dict(id="Exhibit A", measurer="Michael Hart", documents="replay set", computation="per-slice bars",
                          interval="95% Wilson")],
        steps=[("draft", "frontier model", ["draft"]), ("rule check", "deterministic", ["threshold"])],
        claims=[dict(id="amendment terms", history=[(0, "V", False), (40, "F", True)])],
        gate=dict(gate="go-live bars", bar=0.80, judged_on="slices", slices={"clerk": (1, 1)}),
        accuracy=[dict(value="replay test", scorer="customer", documents="customer")],
        adapter=dict(key_reread=True), thresholds=[dict(name="clinical rule", value=1, chosen_by="Michael Hart")],
        models=[dict(name="Azure deployment", version="pinned")],
        flows=[dict(flow=f"F{i}", retention_known=True) for i in range(1, 15)], map_generated=True,
        packs=dict(pinned=True, ok=0, n=0),
        why={"R04": "acceptance test (Exhibit A) names the measurer and the bars",
             "R05": "rules in code; the model drafts",
             "R06": "claims carry status in the decision log",
             "R07": "Michael Hart's bars held per slice (day 153)",
             "R08": "replay test scored by Greystone's clerks and nurse reviewers",
             "R10": "clinical rule owned by Michael Hart",
             "R11": "deployment names a version; auto-upgrade off",
             "R12": "14 flows generated; 0 of 1,800 provider entries hold PHI",
             "R14": "packs pinned by content hash (Chapter 40 model)"}),
    "Pennant": dict(
        id="Pennant", phase="managed service", domain=PN,
        alert_routes=["integration@" + PN, "pennant-oncall@" + PN],
        forwards={"pennant-oncall@" + PN: "night rota at " + NL},
        alert_deviation="night alerts forward to Northlight under the managed-service contract; exit drill passed day 283",
        pilot=dict(start=None, exit_rule_day=None, signed_before=True), smap=PENNANT_NOW, no_deputy=4,
        commitments=[dict(id="matched", measurer="Pennant reconciliation team", documents="carrier invoices",
                          computation="pennant-qs-1.1", interval="95% Wilson")],
        steps=[("FX", "deterministic", ["arithmetic"]), ("match", "deterministic", ["join"]),
               ("read", "small model", ["extract"])],
        claims=[dict(id="matched definition", history=[(119, "D", False), (121, "F", True)])],
        gate=dict(gate="matched (day 133)", bar=0.80, judged_on="slices", slices={"invoices": (1739, 2096)}),
        accuracy=[dict(value="83% matched", scorer="customer", documents="customer")],
        adapter=dict(key_reread=True), thresholds=[dict(name="two-key linkage", value=2, chosen_by="Dana Whitaker")],
        models=[dict(name="extract (europe-west4)", version="extract-2026-01")],
        flows=[dict(flow="EDI 210/214", retention_known=True)], map_generated=True,
        runbooks=[dict(id=f"RB{i}", vendor_steps=0) for i in range(1, 5)], drill="day 283, passed",
        packs=dict(pinned=True, ok=0, n=0),
        why={"R01": "shadow exit criteria signed before shadow",
             "R05": "FX table and two-key match in code; the model reads",
             "R06": "'matched' rose from draft to fact on a signature",
             "R08": "83% matched, scored by Pennant's reconciliation team",
             "R10": "two-key linkage signed by Dana Whitaker",
             "R04": "'matched' signed by Dana Whitaker (day 121)",
             "R07": "matched read per queue; 357 exceptions routed by name",
             "R11": "extract-2026-01 pinned and recorded for europe-west4",
             "R12": "map generated; erasure and retention recorded",
             "R13": "8 vendor-only steps in 4 runbooks fell to 0 (v1)",
             "R14": "packs pinned by content hash (Chapter 40 model)"}),
    "Harbourline": dict(
        id="Harbourline", phase="live", domain="harbourline.example", alert_routes=[],
        pilot=dict(start=None, exit_rule_day=None, signed_before=True), smap=HARBOURLINE_NOW,
        commitments=[dict(id="HA release boundary", measurer="credit review scoring", documents="credit officers' memos",
                          computation="agreement on 600 memos", interval="95% Wilson")],
        steps=[("ratios", "deterministic", ["arithmetic", "threshold"]), ("joins", "deterministic", ["join"]),
               ("draft memo", "frontier model", ["draft"])],
        claims=[dict(id="D-01", history=[(-60, "V", False), (-50, "D", False)])],
        gate=dict(gate="model-risk gate (second submission)", bar=0.80, judged_on="slices",
                  slices={"memos": (546, 600)}),
        accuracy=[dict(value="91% agreement", scorer="customer", documents="customer")],
        adapter=dict(key_reread=True), thresholds=[dict(name="LTV policy", value=0.75, chosen_by="Harbourline credit policy")],
        models=[dict(name="draft", version="pinned")],
        flows=[dict(flow="memo drafts", retention_known=True)], map_generated=True,
        packs=dict(pinned=True, ok=0, n=0),
        why={"R01": "read-and-draft boundary and shadow exit in the contract",
             "R04": "shadow agreement scored by Harbourline credit review",
             "R05": "joins, ratios and thresholds in code; the model drafts",
             "R06": "bid claims D-01 and D-05 rewritten after lint",
             "R07": "model-risk gate green at the second submission",
             "R08": "91% agreement on 600 memos, Harbourline's scoring",
             "R10": "LTV limit set by Harbourline credit policy",
             "R11": "model versions pinned for the committee",
             "R12": "map generated; bid-stage digest retired",
             "R14": "packs pinned by content hash (Chapter 40 model)"}),
}

# Anti-patterns each engagement exposed and closed during the story (story ids above, by engagement).
EXPOSED = {e: [s["rule"] for s in STORIES if s["who"] == e] for e in ("Caldwell", "Greystone", "Pennant", "Harbourline")}
EXPOSED["Greystone"] = ["R02", "R12"]   # the kickoff map (injected case) and the drawn data map
