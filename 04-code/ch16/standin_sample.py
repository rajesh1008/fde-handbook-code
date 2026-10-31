"""STAND-IN for Caldwell's first 200 files (day 47). The real files never leave Caldwell's account.

The manifest columns come from fieldkit's fixture `caldwell_sample()` (seed 47): document type, policy number
(five blank), loss date and OCR confidence (47 below 0.80), exactly the numbers the day-47 readiness report printed
(Chapter 15). The text is rendered by the same generator with the structure Anne Kessler's adjusters see:
agencies writing for clients, forwarded chains, short and written dates, Spanish-language letters, field phrasings,
and highway and landmark locations. Gold values stand in for what her adjusters keyed on days 48 to 51.
"""
import random
import _paths  # noqa: F401
from fieldkit.fixtures import caldwell_sample
from claimsgen import Profile, make_doc

REAL_STRUCTURE = Profile(
    name="Caldwell sample (stand-in)",
    doc_type={},  # taken row by row from the manifest
    channel={"email": 0.45, "fax": 0.30, "mail": 0.25},
    agent_sender=0.30, forwarded=0.25,
    date_style={"mdy4": 0.70, "mdy2": 0.18, "written": 0.12},
    spanish=0.08,
    narrative_pools=("plain", "ambiguous", "field"), pool_weights=(0.45, 0.10, 0.45),
    location_style={"street": 0.70, "highway": 0.20, "landmark": 0.10},
    party_style={"labeled": 0.5, "parenthetical": 0.5},
    injury_style={"plain": 0.7, "field": 0.3})


TEXT_SEED = 4787  # fixed seed for the rendered text; the manifest seed stays 47


def sample(n=200, seed=47):
    rows = caldwell_sample(n=n, seed=seed)
    rng = random.Random(TEXT_SEED)
    docs = []
    for i, r in enumerate(rows):
        base = dict(doc_type=r["doc_type"], policy_number=r["policy_number"], loss_date=r["loss_date"],
                    ocr_confidence=r["ocr_confidence"], claim_id=r["claim_id"], claimant=r["claimant"])
        if r["ocr_confidence"] < 0.80:
            base["channel"] = "fax" if rng.random() < 0.7 else "mail"
        docs.append(make_doc(i, rng, REAL_STRUCTURE, base))
    return docs
