"""Deterministic stand-in for Chapter 35. Every person and record here is invented; no real patient, claimant or
consignee appears. Configurations mirror what the lab's generator would read from each deployed estate."""
import random

from fieldkit.privacy import Hop

SEED = 35
FIRST = ["Ellen", "Marcus", "Teresa", "Victor", "Nadia", "Howard", "Lucia", "Graham", "Irene", "Simon", "Rosa", "Calvin",
         "Martha", "Desmond", "Yvonne", "Albert", "Celia", "Franklin", "Gloria", "Warren"]
LAST = ["Thorpe", "Delgado", "Whitcombe", "Kowalski", "Brandt", "Okonjo", "Ferrante", "Lindqvist", "Ashby", "Moreau",
        "Halvorsen", "Pruitt", "Castellano", "Vance", "Sorensen", "Achebe", "Rourke", "Szabo", "Penrose", "Takeda"]
REASONS = ["knee pain after fall", "suspected sleep apnea", "persistent migraine", "thyroid nodule follow-up",
           "chest pain on exertion", "chronic lower back pain", "abnormal liver panel", "hearing loss, left ear"]

# ----- Greystone: the hand-drawn map Sam approved on day 98 --------------------------------------------------------
GREYSTONE_DRAWN = [
    Hop("referral-intake", "Greystone", ("PHI",), "Greystone Azure", 7, "owner", "store", source="drawn"),
    Hop("drafting-service", "Northlight", ("PHI",), "Greystone Azure", 0, "BAA GA-02", "process", source="drawn"),
    Hop("model-endpoint", "Provider", ("PHI",), "provider US", 0, "BAA GA-02, GA-06", "process", source="drawn"),
    Hop("coordinator-queue", "Greystone", ("PHI",), "EHR", 2190, "owner", "store", source="drawn"),
    Hop("run-records", "Greystone", ("PHI",), "Greystone Azure", 2190, "owner", "store", source="drawn"),
]


def greystone_config(day=122):
    """Deployed configuration as the generator reads it. Day 122 is before the fix; day 125 is after."""
    fixed = day >= 125
    return {"components": [
        {"name": "referral-intake", "holder": "Greystone", "data": ["PHI"], "location": "Greystone Azure",
         "stateless": False, "retention_days": 7, "basis": "owner"},
        {"name": "api-gateway", "holder": "Greystone", "data": ["PHI"], "location": "Greystone Azure", "basis": "owner",
         "stores": [{"name": "gateway-diagnostics", "kind": "log", "body": not fixed, "retention_days": 30}]},
        {"name": "drafting-service", "holder": "Northlight", "data": ["PHI"], "location": "Greystone Azure",
         "basis": "BAA GA-02",
         "stores": [{"name": "app-log", "kind": "log", "body": False, "retention_days": 30},
                    {"name": "trace-export", "holder": "ObsVendor", "kind": "trace", "body": not fixed,
                     "retention_days": 14, "location": "vendor US"}]},
        {"name": "model-endpoint", "holder": "Provider", "data": ["PHI"], "location": "provider US",
         "basis": "BAA GA-02, GA-06",
         "stores": [{"name": "abuse-monitoring", "holder": "Provider", "kind": "log", "retention_days": 30,
                     "basis": "Exhibit C", "signed": "Sam Oakley, day 120"}]
                   + ([] if fixed else [{"name": "stored-requests", "holder": "Provider", "kind": "log",
                                         "retention_days": 30, "basis": ""}])},
        {"name": "guideline-index", "holder": "Greystone", "data": ["POLICY"], "location": "Greystone Azure",
         "basis": "owner"},
        {"name": "coordinator-queue", "holder": "Greystone", "data": ["PHI"], "location": "EHR", "stateless": False,
         "retention_days": 2190, "basis": "owner"},
        {"name": "run-records", "holder": "Greystone", "data": ["PHI"], "location": "Greystone Azure",
         "stateless": False, "retention_days": 2190, "basis": "owner"},
        {"name": "eval-set", "holder": "Greystone", "data": ["PHI"], "location": "Greystone Azure",
         "stateless": False, "retention_days": 120, "basis": "owner"},
        {"name": "support-access", "holder": "Northlight", "data": ["PHI"], "location": "Greystone PAM",
         "basis": "BAA GA-02"},
    ]}


# ----- Greystone sandbox week referrals (days 115 to 119) and what the provider's stored-request log kept -----------
def referrals(n=200):
    rng = random.Random(SEED)
    out = []
    for i in range(n):
        first, last = FIRST[rng.randrange(20)], LAST[rng.randrange(20)]
        out.append({"id": f"R-{1150 + i}", "patient_name": f"{first} {last}", "mrn": f"{rng.randrange(10**6, 10**7):07d}",
                    "dob": f"{rng.randrange(1, 13)}/{rng.randrange(1, 29)}/{rng.randrange(1940, 2005)}",
                    "reason": REASONS[rng.randrange(len(REASONS))], "scanned": rng.random() < 0.4,
                    "narrative_name": rng.random() < 0.3})
    return out


def provider_log(refs, fixed=False):
    """Three calls per referral: classify, extract, draft. The stored-request feature kept request bodies."""
    rng = random.Random(SEED + 1)
    lines = []
    for r in refs:
        last = r["patient_name"].split()[1]
        head = f"MRN {r['mrn']} DOB: {r['dob']} " if r["scanned"] else ""
        narr = f"Ms. {last} reports {r['reason']}." if r["narrative_name"] else f"Patient reports {r['reason']}."
        bodies = [f"classify: {narr}", f"extract: {head}{narr}", f"draft: referral {r['id']} {r['reason']}"]
        for b in bodies:
            if fixed:
                lines.append(f"req={rng.randrange(16**8):08x} model=pinned tokens={rng.randrange(300, 2400)} status=200")
            else:
                lines.append(f"req={rng.randrange(16**8):08x} body=\"{b}\"")
    return lines


def known_values(refs):
    """Greystone's roster of the period's patients, one known-value table."""
    return [{f"p{i}_name": r["patient_name"] for i, r in enumerate(refs)}]


# ----- Greystone minimum necessary: the referral packet's fields ---------------------------------------------------
PACKET_FIELDS = ["patient_name", "mrn", "dob", "address", "phone", "insurance_member_id", "ssn_last4", "referring_provider",
                 "specialty", "reason", "icd10_codes", "urgency", "prior_imaging", "medications", "allergies",
                 "full_history"]
NEEDED_FIELDS = ["specialty", "reason", "icd10_codes", "urgency", "prior_imaging", "medications", "allergies"]

# ----- Caldwell: claims, Connecticut insurer, policyholders in California --------------------------------------------
CALDWELL = [
    Hop("claim-files", "Northlight", ("CLAIM-PI",), "Caldwell AWS us-east-1", 90, "CA-15", "store"),
    Hop("shadow-runner", "Northlight", ("CLAIM-PI",), "Caldwell AWS us-east-1", 0, "CA-15", "process"),
    Hop("gateway-logs", "Caldwell", ("META",), "Caldwell AWS us-east-1", 30, "owner", "log"),
    Hop("model-endpoint", "Provider", ("CLAIM-PI",), "provider US", 0, "CA-10, Exhibit D", "process"),
    Hop("run-records", "Caldwell", ("CLAIM-PI",), "Caldwell AWS us-east-1", 2555, "CA-07", "store"),
    Hop("support-access", "Northlight", ("CLAIM-PI",), "nl-shadow-readers", 0, "CA-15", "access"),
    Hop("C06-ft1-weights", "Caldwell", ("CLAIM-PI",), "Caldwell AWS us-east-1", None, "owner", "weights",
        deletable=False),
]

# ----- Pennant: EU shipments, GDPR, processor terms -----------------------------------------------------------------
def pennant(fixed=False):
    return [
        Hop("eu-shipment-records", "Pennant", ("EU-PI",), "Pennant ERP", 3650, "owner", "store"),
        Hop("match-service", "Northlight", ("EU-PI",), "GCP europe-west4", 0, "DPA PA-01", "process"),
        Hop("model-endpoint", "Provider", ("EU-PI",), "provider europe-west4", 0, "DPA PA-02", "process"),
        Hop("match-cache", "Northlight", ("EU-PI",), "GCP europe-west4", 14, "DPA PA-01", "cache"),
        Hop("eval-set", "Northlight", ("EU-PI",), "GCP europe-west4", 180, "DPA PA-03", "store"),
        Hop("run-records", "Northlight", ("EU-PI",) if not fixed else ("META",), "GCP europe-west4", 365, "DPA PA-03",
            "store", deletable=False),
        Hop("gateway-logs", "Northlight", ("META",), "GCP europe-west4", 30, "DPA PA-01", "log"),
    ] + ([Hop("run-subject-fields", "Northlight", ("EU-PI",), "GCP europe-west4", 365, "DPA PA-03", "store")]
         if fixed else []) + [
        Hop("backups", "Northlight", ("EU-PI",), "GCP europe-west4", 28 if fixed else 35, "DPA PA-03", "backup",
            deletable=False),
        Hop("oncall-access", "Northlight", ("EU-PI",), "on-call outside EEA", 0, "DPA PA-04", "access",
            region_ok=False, transfer="SCCs + TIA, pseudonymized view" if fixed else ""),
    ]
