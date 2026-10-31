"""Customer fixtures: the four Northlight engagements, reproducible from a seed. All names are fictional."""
import random
from .access import AccessRequest, AccessTracker
from .readiness import ReadinessRegister

CUSTOMERS = {
    "caldwell": dict(name="Caldwell Mutual", city="Hartford", cloud="AWS", contract="$1.6M/yr"),
    "greystone": dict(name="Greystone Health", city="Denver", cloud="Azure", contract="$2.4M/yr"),
    "pennant": dict(name="Pennant Logistics", city="Memphis", cloud="GCP", contract="$740k/yr"),
    "harbourline": dict(name="Harbourline Bank", city="Toronto", cloud="private + Azure", contract="C$1.9M/yr"),
}

DOC_TYPES = ["first notice of loss", "adjuster note", "repair estimate", "police report", "medical bill", "photo log"]


def caldwell_tracker():
    t = AccessTracker("Caldwell Mutual")
    t.add(AccessRequest("synthetic-claims-set", "synthetic claim files built from the schema", "synthetic",
                        "Northlight (us)", 1, "granted", 6))
    t.add(AccessRequest("aws-sandbox-account", "isolated AWS account in Caldwell's org", "synthetic",
                        "Daniel Reyes", 2, "granted", 19))
    t.add(AccessRequest("gateway-key", "model gateway key", "sampled", "Priya Natarajan", 4, "granted", 33,
                        expires_every=7))
    t.add(AccessRequest("claims-sample-200", "200 de-identified claim files", "sampled", "Anne Kessler", 9,
                        "granted", 47))
    t.add(AccessRequest("sample-storage-decision", "where the sample is stored and for how long", "sampled",
                        "Priya Natarajan", 47, "requested", next_action="answer storage question today",
                        blocks=["eval set v1"]))
    t.add(AccessRequest("claims-core-readonly", "read-only service account on the claims core", "shadowed",
                        "Daniel Reyes", 5, "in review", next_action="architecture review slot",
                        blocks=["shadow feed", "integration tests"]))
    t.add(AccessRequest("adjuster-sso-group", "SSO group for twelve pilot adjusters", "shadowed",
                        "Anne Kessler", 30, "requested", next_action="name the twelve adjusters",
                        blocks=["shadow feed"]))
    t.add(AccessRequest("prod-change-window", "production change window", "live", "Daniel Reyes", None,
                        "not requested"))
    return t


def greystone_tracker():
    t = AccessTracker("Greystone Health")
    t.add(AccessRequest("synthetic-referrals", "synthetic referral packets", "synthetic", "Northlight (us)", 1,
                        "granted", 8))
    t.add(AccessRequest("azure-subscription", "Azure subscription with private endpoints", "synthetic",
                        "Sam Oakley", 3, "in review", next_action="security questionnaire answers",
                        blocks=["deploy", "referral sample"]))
    t.add(AccessRequest("referral-sample", "de-identified referral packets", "sampled", "Michael Hart", 10,
                        "requested", next_action="privacy officer sign-off", blocks=["eval set v1"]))
    return t


def pennant_tracker():
    t = AccessTracker("Pennant Logistics")
    t.add(AccessRequest("edi-sample", "a week of EDI 214 messages", "sampled", "Jenna Ruiz", 2, "granted", 11))
    t.add(AccessRequest("gcp-project", "GCP project in Pennant's org", "synthetic", "Jenna Ruiz", 1, "granted", 5))
    return t


def harbourline_tracker():
    t = AccessTracker("Harbourline Bank")
    t.add(AccessRequest("synthetic-statements", "synthetic financial statements", "synthetic", "Northlight (us)",
                        1, "granted", 4))
    t.add(AccessRequest("model-risk-intake", "model-risk inventory entry", "sampled", "Helen Marsh", 6,
                        "in review", next_action="tiering memo", blocks=["any real statement"]))
    return t


TRACKERS = dict(caldwell=caldwell_tracker, greystone=greystone_tracker, pennant=pennant_tracker,
                harbourline=harbourline_tracker)


def caldwell_sample(n=200, seed=47, drop_column=None):
    """The first real delivery, as its manifest arrives: one row per claim file."""
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        row = dict(claim_id=f"CM-{2026_00000 + 3 * i + rng.randint(0, 2):010d}",
                   policy_number=f"HP{rng.randint(100000, 999999)}",
                   loss_date=f"2026-{rng.randint(1, 8):02d}-{rng.randint(1, 28):02d}",
                   doc_type=rng.choice(DOC_TYPES),
                   pages=rng.choice([1, 1, 2, 3, 4, 6, 9, 14, 22]),
                   ocr_confidence=round(rng.betavariate(9, 1.4), 3),
                   claimant="Emily Carter" if i == 0 else f"claimant {i:03d}")
        if rng.random() < 0.05:
            row["policy_number"] = ""
        if drop_column:
            row.pop(drop_column, None)
        rows.append(row)
    return rows


def caldwell_register():
    reg = ReadinessRegister()
    reg.register("caldwell-claims-sample", key="claim_id",
                 required=["policy_number", "loss_date", "doc_type", "pages"],
                 checks={"OCR confidence >= 0.80": lambda r: r.get("ocr_confidence", 0) >= 0.80},
                 min_rows=150)
    return reg
