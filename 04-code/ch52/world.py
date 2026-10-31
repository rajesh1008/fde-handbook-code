"""Chapter 52 lab world: Caldwell's evaluation suite rerun on a model two generations newer than the pin.

Deterministic stand-in. No model calls. Every model behavior below is a seeded function of (version, document,
field); the numbers are the lab's, not Caldwell's production numbers. Version names gm-n1 and gm-n2 are lab
labels for "one generation" and "two generations" after the pin gm-2026-05-14 (Chapter 24).
"""
import random, hashlib

PIN, N1, N2 = "gm-2026-05-14", "gm-n1", "gm-n2"
VERSIONS = (PIN, N1, N2)
FIELDS = ("claimant_name", "policy_number", "loss_date", "date_received", "loss_location", "loss_type",
          "vehicle_vin", "police_report", "injury_flag", "attorney_flag")
DETERMINISTIC = ("policy_number", "date_received", "vehicle_vin")   # rules, lookups and checksums, no model
MODEL_FIELDS = tuple(f for f in FIELDS if f not in DETERMINISTIC)
CRITICAL = ("policy_number", "loss_date", "date_received", "injury_flag")
WEIGHT = {f: (3 if f in CRITICAL else 1) for f in FIELDS}
TEST_DOCS = [f"G{n:03d}" for n in range(100, 301)]          # gold-set-300 test split: 201 documents
CAL_DOCS = [f"K{n:03d}" for n in range(600)]                # cal-600 (Chapter 27): even fit, odd check

# per-version skill on model fields (probability a field is right), cost and latency
SKILL = {PIN: {"claimant_name": .97, "loss_date": .90, "loss_location": .80, "loss_type": .86,
               "police_report": .88, "injury_flag": .91, "attorney_flag": .89},
         N1: {"claimant_name": .975, "loss_date": .915, "loss_location": .82, "loss_type": .88,
              "police_report": .89, "injury_flag": .92, "attorney_flag": .90},
         N2: {"claimant_name": .98, "loss_date": .93, "loss_location": .85, "loss_type": .90,
              "police_report": .91, "injury_flag": .94, "attorney_flag": .92}}
NOISE = {PIN: 0.0, N1: 0.035, N2: 0.05}       # how much a version's errors differ item by item from the pin's
COST = {PIN: 0.0112, N1: 0.0079, N2: 0.0051}  # model dollars per document, intake summary included
P95 = {PIN: 3.8, N1: 3.1, N2: 2.4}            # seconds
SUMMARY_TOKENS = {PIN: 212, N1: 190, N2: 131}
INFLATE = {PIN: 0.0, N1: 0.01, N2: 0.18}      # stated-confidence shift on the hard items (behavior change 1)
DROP_QUALIFIER = {PIN: 0, N1: 1, N2: 12}      # dispute statements omitted from summaries (behavior change 2)


def u(*key):
    h = hashlib.sha256("|".join(map(str, key)).encode()).hexdigest()
    return int(h[:12], 16) / 16 ** 12


def correct(version, doc, field):
    if field in DETERMINISTIC:
        return u("det", doc, field) > 0.004            # the rules miss the same rare items for every model
    return margin(version, doc, field) > 0


def margin(version, doc, field):
    d = u("difficulty", doc, field)
    jitter = (u("noise", version, doc, field) - 0.5) * 2 * NOISE[version]
    return SKILL[version][field] - (d + jitter)          # positive means the field is right


def stated(version, doc, field):
    """The confidence the model states: a noisy reading of how far the item is from the model's error boundary.
    Calibrated for the pin; gm-n2 states more on the items near its boundary (behavior change 1)."""
    m = margin(version, doc, field)
    s = 0.62 + 1.6 * m + (u("conf", version, doc, field) - 0.5) * 0.40
    if m < 0.06:
        s += INFLATE[version]
    return round(min(0.999, max(0.01, s)), 4)


def scored(version, docs=TEST_DOCS):
    return {(d, f): correct(version, d, f) for d in docs for f in FIELDS}


# 34 of the 201 test documents contain a dispute statement ("claimant disputes liability", "coverage under review")
DISPUTE_DOCS = sorted(TEST_DOCS, key=lambda d: u("dispute", d))[:34]


def summary_keeps_dispute(version, doc):
    order = sorted(DISPUTE_DOCS, key=lambda d: u("drop", d))
    return doc not in order[:DROP_QUALIFIER[version]]
