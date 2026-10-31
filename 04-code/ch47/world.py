"""Chapter 47 world: Northlight's FDE function at twenty customers (function months 13 to 18).

Deterministic, labeled stand-in. The four named customers keep their story facts (Caldwell AWS with a seven-day
gateway key rotation, Greystone Azure, Pennant Google Cloud, Harbourline a bank in build). Customers N05 to N20 are
numbered stand-ins for the engagements Northlight signed after Caldwell went live. Every count, hour and month here
is replayed exactly so the outputs in the chapter reproduce. No model calls.
"""
NAMED = {"N01": "Caldwell", "N02": "Greystone", "N03": "Pennant", "N04": "Harbourline"}

# id: (sector, workflow, cloud, gateway, pod, phase at month 18, start month)
ENGAGEMENTS = {
    "N01": ("insurance", "claims-intake", "aws", "aws-gw", "A", "retained duties", 0),
    "N02": ("health", "referral-intake", "azure", "apim", "B", "shadow", 1),
    "N03": ("logistics", "doc-reconciliation", "gcp", "apigee", "B", "managed service", 1),
    "N04": ("banking", "kyc-review", "azure", "apim", "A", "build", 8),
    "N05": ("insurance", "claims-intake", "aws", "aws-gw", "A", "handed over", 11),
    "N06": ("health", "referral-intake", "azure", "apim", "B", "shadow", 12),
    "N07": ("public", "permit-review", "onprem", "none", "B", "build", 13),
    "N08": ("insurance", "claims-intake", "azure", "apim", "A", "live", 12),
    "N09": ("logistics", "doc-reconciliation", "aws", "kong", "B", "live", 12),
    "N10": ("insurance", "claims-intake", "gcp", "apigee", "A", "live", 13),
    "N11": ("health", "referral-intake", "aws", "litellm", "B", "build", 13),
    "N12": ("banking", "kyc-review", "aws", "aws-gw", "A", "build", 14),
    "N13": ("utility", "correspondence", "onprem", "none", "B", "discovery", 15),
    "N14": ("logistics", "doc-reconciliation", "gcp", "apigee", "B", "shadow", 14),
    "N15": ("insurance", "claims-intake", "aws", "aws-gw", "A", "live", 14),
    "N16": ("health", "referral-intake", "azure", "apim", "B", "build", 15),
    "N17": ("insurance", "claims-intake", "onprem", "none", "A", "shadow", 15),
    "N18": ("banking", "kyc-review", "azure", "apim", "A", "discovery", 16),
    "N19": ("logistics", "doc-reconciliation", "aws", "litellm", "B", "build", 16),
    "N20": ("health", "referral-intake", "gcp", "apigee", "B", "discovery", 17),
}
IDS = list(ENGAGEMENTS)
def name(e): return NAMED.get(e, e)
def by(pred): return [e for e, v in ENGAGEMENTS.items() if pred(v)]

HAS_GW = by(lambda v: v[3] != "none")
DOCS = by(lambda v: v[0] in ("insurance", "logistics", "health"))[:11]

# ---- what repeats: (component, engagements, shape function, bespoke hours per engagement) ---------------------
def _inst():
    rows = []
    def add(comp, engs, shape, hours):
        for e in engs:
            rows.append((e, comp, shape(e), hours(e) if callable(hours) else hours))
    sec = lambda e: ENGAGEMENTS[e][0]
    add("evaluation suite runner", IDS, lambda e: "fieldkit", 60)
    add("estate adapter per cloud", IDS, lambda e: ENGAGEMENTS[e][2], 30)
    add("gateway adapter", IDS, lambda e: "gateway" if e in HAS_GW else "direct via proxy", 40)
    add("alert routes and runbook", IDS, lambda e: "managed" if e == "N03" else "customer rota", 24)
    add("audit log, hash-chained", [e for e in IDS if e not in ("N07", "N13")], lambda e: "fieldkit", 16)
    add("gateway key refresh on 401", HAS_GW, lambda e: "fieldkit", 22)
    add("shadow tap", [e for e in IDS if e not in ("N13", "N18", "N20", "N07")],
        lambda e: {"health": "fhir", "logistics": "file"}.get(sec(e), "queue"), 20)
    add("upfront document quality gate", DOCS, lambda e: "pages" if sec(e) != "logistics" else "edi+pages", 64)
    add("connector to the system of record", IDS,
        lambda e: {"N05": "guidewire", "N15": "guidewire", "N09": "sftp", "N19": "sftp", "N11": "fhir-api",
                   "N16": "fhir-api"}.get(e, "own-" + e), 120)
    add("sponsor dashboard", [e for e in IDS if e not in ("N13", "N18", "N20", "N07", "N17", "N16")],
        lambda e: "own-" + e if e != "N10" else "own-N08", 30)
    add("permission-inheriting retrieval", by(lambda v: v[0] in ("banking", "health")) + ["N01"],
        lambda e: {"azure": "sharepoint", "aws": "s3-acl", "gcp": "drive"}[ENGAGEMENTS[e][2]], 40)
    add("claims first-notice extraction", by(lambda v: v[1] == "claims-intake"),
        lambda e: "acord" if e != "N17" else "acord-onprem", 90)
    add("referral packet intake, draft-only", by(lambda v: v[1] == "referral-intake"),
        lambda e: "fhir" if e != "N02" else "fax+fhir", 110)
    add("shipment document reconciliation", by(lambda v: v[1] == "doc-reconciliation"), lambda e: "x12+pdf", 100)
    add("KYC document review", by(lambda v: v[1] == "kyc-review"), lambda e: "own-" + e, 140)
    add("claims-core write-back", ["N01"], lambda e: "own-N01", 180)
    add("permit rules engine", ["N07"], lambda e: "own-N07", 160)
    return rows
INSTANCES = _inst()

# ---- playbooks -------------------------------------------------------------------------------------------------
VAULTS = {"aws-secrets", "azure-kv", "gcp-sm", "hashicorp"}
GATEWAYS = {"aws-gw", "apim", "apigee", "kong", "litellm", "fieldkit-direct"}
def PB1(version, declare_gateway):
    from fieldkit.playbooks import Playbook, Step
    s4 = dict(gateway=GATEWAYS) if declare_gateway else {}
    return Playbook("PB-1", version, "Claims first-notice intake", "Caldwell", "Callum Reid", "claims-intake", [
        Step("PB-1.S1", "Map first-notice fields to the claims system's intake schema", "FDE", "pb1/test_schema.py"),
        Step("PB-1.S2", "Load the 300-claim gold set with the customer's claims data owner", "FDE + customer",
             "pb1/test_gold.py"),
        Step("PB-1.S3", "Store the model key in the customer's vault and grant the runner read", "FDE",
             "pb1/test_secret.py", dict(vault=VAULTS)),
        Step("PB-1.S4", "Register the intake route on the customer's model gateway with the pinned deployment",
             "FDE", "pb1/test_route.py", s4),
        Step("PB-1.S5", "Run the shadow week and score it with the evaluation suite", "FDE + customer",
             "pb1/test_shadow.py"),
        Step("PB-1.S6", "Move alert routes to the claims operations rota", "customer", "pb1/test_routes.py"),
    ], proven_at=["N01", "N05", "N08", "N10", "N15"], maturity="live")

def PB2(version, declare):
    from fieldkit.playbooks import Playbook, Step
    return Playbook("PB-2", version, "Shipment document reconciliation", "Pennant", "Sofia Brennan",
                    "doc-reconciliation", [
        Step("PB-2.S1", "Read carrier invoices from the object store drop", "FDE", "pb2/test_drop.py",
             dict(object_store={"s3", "gcs", "blob"}) if declare else {}),
        Step("PB-2.S2", "Score every document with the upfront quality gate before matching", "FDE",
             "pb2/test_quality.py"),
        Step("PB-2.S3", "Check X12 envelopes and reconcile against the transport system export", "FDE",
             "pb2/test_x12.py", dict(edi={"x12"})),
        Step("PB-2.S4", "Agree the written definition of matched with the reconciliation lead", "customer",
             "pb2/test_definition.py"),
    ], proven_at=["N03", "N09"], maturity="live")

def PB3(version, declare):
    from fieldkit.playbooks import Playbook, Step
    return Playbook("PB-3", version, "Referral intake, draft-only", "Greystone", "Aisha Rahman", "referral-intake", [
        Step("PB-3.S1", "Map referral packets to FHIR resources", "FDE", "pb3/test_map.py",
             dict(fhir={"r4"}) if declare else {}),
        Step("PB-3.S2", "Draft the prior-authorization summary, never submit it", "FDE", "pb3/test_draft_only.py"),
        Step("PB-3.S3", "Route drafts to the clinical reviewer queue with the source pages attached", "customer",
             "pb3/test_review.py"),
    ], proven_at=[], maturity="shadow")

def PB4():
    from fieldkit.playbooks import Playbook, Step
    return Playbook("PB-4", "2.0", "Model access onboarding", "Caldwell and N07", "Jonah Webb", "any", [
        Step("PB-4.S1", "Inventory the model path: customer gateway, egress proxy, or neither", "FDE",
             "pb4/test_inventory.py", dict(gateway=GATEWAYS | {"none"})),
        Step("PB-4.S2", "With no customer gateway, run the fieldkit adapter in direct mode behind the egress proxy",
             "FDE", "pb4/test_direct.py", dict(egress_proxy={"yes"}, gateway={"none"})),
        Step("PB-4.S3", "Store the key in the customer's vault with a rotation schedule", "FDE", "pb4/test_rotation.py",
             dict(vault=VAULTS)),
        Step("PB-4.S4", "Write the route record that later playbook steps read", "FDE", "pb4/test_record.py"),
    ], proven_at=["N07"], maturity="live")

ESTATE = {e: dict(cloud=v[2], gateway=v[3], vault={"aws": "aws-secrets", "azure": "azure-kv", "gcp": "gcp-sm",
                                                    "onprem": "hashicorp"}[v[2]],
                  egress_proxy="yes" if v[2] == "onprem" else "no",
                  object_store={"aws": "s3", "azure": "blob", "gcp": "gcs", "onprem": "none"}[v[2]],
                  edi="x12" if v[1] == "doc-reconciliation" else "none", fhir="r4" if v[0] == "health" else "none")
          for e, v in ENGAGEMENTS.items()}

# ---- engagement manifests (month 15 as found, month 18 after the fixes) -------------------------------------------
def manifests(month):
    from copy import deepcopy
    pbmap = {"claims-intake": "PB-1@1.3", "doc-reconciliation": "PB-2@1.1", "referral-intake": "PB-3@0.9"}
    out = []
    for e, (sec, wf, cloud, gw, pod, phase, start) in ENGAGEMENTS.items():
        m = dict(id=e, playbook=pbmap.get(wf), adapter="fieldkit.gateway", eval_suite=True,
                 gold_owner="named", phase=phase, customer_domain=f"{e.lower()}.example",
                 alert_routes=[f"oncall@{e.lower()}.example"], deviations=[], fieldkit_layer=5.4, needs_layer=5.0,
                 secrets_owner="customer")
        if wf in ("kyc-review", "permit-review", "correspondence"):
            m["deviations"].append(dict(what="playbook", reason=f"no playbook for {wf} yet", owner="Laura Finch",
                                        review_by=19))
        if phase in ("managed service",):
            m["alert_routes"] = ["fde-oncall@northlight.ai"]
        out.append(m)
    M = {m["id"]: m for m in out}
    if month == 15:
        M["N05"]["playbook"] = "PB-1@1.1"
        M["N06"]["playbook"] = None
        M["N13"]["deviations"] = []
        M["N20"]["playbook"] = "PB-3@0.8"
        for e in ("N08", "N12", "N16"):
            M[e]["adapter"] = f"copy of gateway.py ({e})"
        M["N13"]["adapter"] = "direct, vendor SDK"
        M["N07"]["adapter"] = "direct, vendor SDK"
        M["N07"]["deviations"].append(dict(what="adapter", reason="no customer gateway", owner="", review_by=18))
        M["N09"]["gold_owner"] = ""
        M["N18"]["gold_owner"] = ""
        M["N14"]["eval_suite"] = False
        M["N05"]["alert_routes"].append("callum.reid@northlight.ai")
        M["N11"]["deviations"].append(dict(what="retrieval", reason="ACL export pending", owner="Aisha Rahman",
                                           review_by=12))
        M["N10"]["fieldkit_layer"] = 4.5
        M["N15"]["fieldkit_layer"] = 4.7
        M["N13"]["secrets_owner"] = "northlight"
        M["N17"]["playbook"] = "PB-1@1.3"
    else:  # month 18: fixes made; two registered deviations remain, both dated
        for e in ("N07", "N13", "N17"):
            M[e]["adapter"] = "fieldkit.gateway"   # direct mode through PB-4
        M["N12"]["adapter"] = "bank SDK wrapper"
        M["N12"]["deviations"].append(dict(what="adapter", reason="bank mandates its own SDK until month 21",
                                           owner="Laura Finch", review_by=21))
        for m in M.values():
            if m["playbook"] == "PB-1@1.3":
                m["playbook"] = "PB-1@1.4"
            if m["playbook"] == "PB-2@1.1":
                m["playbook"] = "PB-2@1.2"
            if m["playbook"] == "PB-3@0.9":
                m["playbook"] = "PB-3@0.9.1"
    return [deepcopy(m) for m in out]

# ---- the product loop -------------------------------------------------------------------------------------------
REPORTS = [  # rid, title, origin, n engagements, median-ish hours list, votes, acv_usd, artifact, first month
    ("FR-001", "gateway key re-read on 401 and refresh", "N01", HAS_GW, 22, 1, 1_600_000,
     "fieldkit/gateway.py + test_v23_ch18.py", 1),
    ("FR-002", "upfront document quality gate with request-back", "N03", DOCS, 64, 2, 740_000,
     "fieldkit/quality.py + test_v26_ch21.py", 5),
    ("FR-003", "sponsor dashboard theming per customer", "N12", ["N12", "N04", "N18"], 17, 9, 2_200_000, "", 14),
    ("FR-004", "alert route ownership check", "N01", IDS[:12], 6, 0, 1_600_000,
     "fieldkit/handover.py + test_v5_ch41.py", 11),
    ("FR-005", "permission-inheriting retrieval for document stores", "N02",
     ["N01", "N02", "N04", "N06", "N11", "N12", "N16", "N18", "N20"], 40, 2, 2_400_000,
     "fieldkit/retrieval.py + test_v3_ch23.py", 6),
    ("FR-006", "on-behalf-of token broker", "N01", ["N01", "N04", "N05", "N08", "N10", "N12", "N15"], 35, 1,
     1_600_000, "fieldkit/surface.py + tests", 9),
    ("FR-007", "Spanish-language claims extraction", "N10", ["N10", "N15"], 80, 4, 1_100_000, "", 15),
    ("FR-008", "X12 envelope checks", "N03", ["N03", "N09", "N14", "N19"], 18, 0, 740_000,
     "fieldkit/connectors.py + test_v24_ch19.py", 4),
    ("FR-009", "SSO group sync for reviewers", "N08", IDS[:14], 9, 3, 900_000, "", 13),
    ("FR-010", "branded PDF export of the evidence pack", "N05", ["N05", "N08", "N10", "N12", "N15", "N04"], 14,
     5, 1_300_000, "", 14),
    ("FR-011", "canary scan on the shadow tap", "N02", IDS[:16], 10, 0, 2_400_000,
     "fieldkit/shadow.py + test_v21_ch16.py", 3),
    ("FR-012", "model pin that refuses regional substitution", "N02", ["N01", "N02", "N03", "N06", "N09", "N14"], 12,
     0, 2_400_000, "fieldkit/estates.py + test_v25_ch20.py", 7),
]
# Two features shipped from the field (product release month; hours per adopting engagement before and after).
SHIPPED = [
    dict(rid="FR-001", feature="Gateway connections: key read at call time, refresh on 401", first_month=1,
         triaged_month=13, shipped_month=14, adopted=HAS_GW, hours_before=22, hours_after=2),
    dict(rid="FR-002", feature="Document quality gate with request-back", first_month=5, triaged_month=13,
         shipped_month=16, adopted=[e for e in DOCS if e not in ("N02", "N06")], hours_before=64, hours_after=12),
]

# ---- time to production by playbook adoption order (days from signature to Live Stable; Caldwell's day 158) ------
TTP = {
    "PB-1 claims intake": [("N01", 158), ("N05", 96), ("N08", 71), ("N10", 55), ("N15", 44), ("N17", 58)],
    "PB-2 document reconciliation": [("N09", 88), ("N19", 61)],
}
N17_LOST = 9   # days lost at N17 to the undeclared gateway step (day 23 to day 31)

# FDE hours per engagement by layer, by cohort (hours-ledger task codes; signature to Live Stable).
HOURS = {
    "first four (N01 to N04)": dict(bespoke=2900, playbook=0, platform=0),
    "months 11 to 14 (N05 to N12)": dict(bespoke=980, playbook=520, platform=140),
    "months 15 to 18 (N13 to N20)": dict(bespoke=610, playbook=330, platform=110),
}
# Monthly FDE hours by phase: (playbook-led, bespoke on the platform, bespoke with no platform). Laura Finch's
# month-18 plan from the hours ledger, months 13 to 18.
PHASE_HOURS = {"discovery": (30, 45, 60), "build": (60, 110, 150), "shadow": (25, 50, 80), "live": (12, 25, 50),
               "handed over": (4, 6, 10), "retained duties": (8, 10, 12), "managed service": (30, 35, 40)}
FIELD_HOURS_PER_FDE = 140   # field hours a month per FDE after travel, internal and platform time
FDES = ["lead FDE", "Callum Reid", "Sofia Brennan", "Aisha Rahman", "Leo Martens", "Imogen Clarke"]

# ---- pods, rotation and the customer's view ---------------------------------------------------------------------
# (customer, month, outgoing anchor, incoming anchor, overlap working days, notice days)
CHANGES_BEFORE = [  # months 13 to 15, before the anchor rule
    ("N08", 13, "Leo Martens", "Imogen Clarke", 0, 3), ("N08", 14, "Imogen Clarke", "Sofia Brennan", 2, 5),
    ("N08", 15, "Sofia Brennan", "Leo Martens", 0, 0), ("N05", 14, "Sofia Brennan", "Leo Martens", 10, 30),
    ("N02", 13, "Callum Reid", "Aisha Rahman", 15, 45), ("N09", 14, "Leo Martens", "Sofia Brennan", 4, 12),
    ("N10", 15, "Imogen Clarke", "Callum Reid", 6, 9),
]
CHANGES_AFTER = [  # months 16 to 18, anchor rule in force
    ("N12", 16, "lead FDE", "Imogen Clarke", 10, 40), ("N14", 17, "Aisha Rahman", "Callum Reid", 12, 35),
    ("N09", 18, "Sofia Brennan", "Leo Martens", 10, 31),
]
