"""Chapter 40 world: Caldwell's live decision records, days 158 to 215.

Deterministic, labeled stand-in: no model calls, no customer data. The stand-in model is a pure function of the
document and the prompt text it was given, plus a seeded rerun wobble on the one judgment field (loss_location),
so that "rerun the model" can be compared honestly with "replay the record".

Story anchors (style sheet): live day 158 (Ch39), router v1.1 proceed 0.95 / floor 0.47 (Ch27), embed-2026-02 and
CM-WL-07 v3 (Ch23), run records kept 2,555 days under CA-07 (Ch35), gateway traces 30 days (Ch35).
Chapter 40 additions (ledgered): parameter-store hotfix day 166 02:10, disputed claim day 169, dispute day 176,
rehearsal day 177, pinning day 180, backfill day 181, architects' review day 184, audit fieldwork 201 to 210,
report day 214.
"""
import random, re
import _paths  # noqa: F401
from fieldkit.lineage import digest

LIVE, HOTFIX_DAY, HOTFIX_MIN, DISPUTE, REHEARSAL, FIX, BACKFILL, REVIEW, AUDIT0, AUDIT1, REPORT, END = (
    158, 166, 130, 176, 177, 180, 181, 184, 201, 210, 214, 215)
PER_DAY = 375
COMMIT = "c7e41a2"                 # code commit the v0 run record carried
MODEL_PIN = "gm-2026-05-14"        # pinned since Ch24; the provider-reported version string
ROUTER = {"name": "router v1.1", "proceed": 0.95, "floor": 0.47, "signed_by": "Anne Kessler", "day": 151}
ROUTER_ID = f"router-v1.1@{digest(ROUTER)}"
INDEX_ID = "nl-index@embed-2026-02@" + digest(["CM-WL-07 v3", "snapshot day 156"])
TRACE_DAYS, RUN_RECORD_DAYS = 30, 2555

BASE = ("You draft first-notice intake fields for Caldwell Mutual claims. Use only the documents provided and the "
        "manual passages retrieved. For every field give the value, the page it came from and the passage that "
        "supports it. If a field is not in the documents, write NOT FOUND; never guess. ")
RULE_A = ("loss_location: the address where the loss occurred as stated by the claimant.")
RULE_B = ("loss_location: if a police report is attached, use the incident address on the police report; otherwise "
          "use the address where the loss occurred as stated by the claimant. Never use the claimant's mailing "
          "address unless the claimant states the loss happened there.")
PROMPT_A, PROMPT_B = BASE + RULE_A, BASE + RULE_B
# Parameter store history: the store keeps every version with its timestamp, whoever wrote it.
PARAM_HISTORY = [(1, 156, 0, PROMPT_A, "release rc-1"), (2, HOTFIX_DAY, HOTFIX_MIN, PROMPT_B, "on-call hotfix, incident ticket")]
REGISTRY = {f"intake-summary@{digest(PROMPT_A)}": PROMPT_A, f"intake-summary@{digest(PROMPT_B)}": PROMPT_B}
ID_B = f"intake-summary@{digest(PROMPT_B)}"


def tokens(s):
    return len(re.findall(r"\w+|[^\w\s]", s))


def prompt_at(day, minute):
    text = None
    for _, d, m, t, _w in PARAM_HISTORY:
        if (day, minute) >= (d, m):
            text = t
    return text


def model(doc, prompt, rerun_seed=None):
    """Stand-in model: loss_location depends on the prompt rule when both addresses are present."""
    if doc["police"] and doc["both"]:
        loc = doc["police_addr"] if "police report" in prompt else doc["letter_addr"]
    else:
        loc = doc["letter_addr"]
    if rerun_seed is not None and random.Random(str(rerun_seed)).random() < 0.015:
        loc = doc["letter_addr"] if loc == doc["police_addr"] else (doc["police_addr"] or loc + " (unit)")
    return {"loss_location": loc, "date_received": doc["date_received"], "doc_type": doc["doc_type"],
            "police_report_ref": doc["police_ref"] or "NOT FOUND"}


def band(score):
    return "proceed" if score >= ROUTER["proceed"] else ("review" if score >= ROUTER["floor"] else "escalate")


def _doc(rng, d, i):
    police = rng.random() < 0.41
    both = police and rng.random() < 0.56
    street = rng.choice(["Farmington Ave", "Asylum St", "Park St", "Franklin Ave", "Wethersfield Ave", "Main St"])
    letter = f"{rng.randint(10, 999)} {street}, Hartford CT"
    pol = (f"{rng.choice(['Capitol Ave', 'Broad St', 'Sigourney St'])} at {rng.choice(['Laurel St', 'Babcock St'])}, Hartford CT"
           if both else (letter if police else None))
    body = rng.randint(380, 2200)
    return {"sha256": digest(["doc", d, i]) + digest(["doc2", d, i])[:4], "pages": rng.randint(1, 9),
            "doc_type": rng.choices(["FNOL form", "claimant letter", "police report", "attorney letter"], [52, 26, 14, 8])[0],
            "police": police, "both": both, "letter_addr": letter, "police_addr": pol,
            "police_ref": f"HPD-26-{rng.randint(10000, 99999)}" if police else None,
            "date_received": f"day {d}", "doc_tokens": body}


def records(start=LIVE, end=END):
    out, lost_n = [], 0
    for d in range(start, end + 1):
        for i in range(PER_DAY):
            rng = random.Random(d * 100000 + i)
            minute = i * 1440 // PER_DAY
            doc = _doc(rng, d, i)
            sent = prompt_at(d, minute)
            out_fields = model(doc, sent)
            r = rng.random()
            score = (0.95 + rng.random() * 0.049) if r < 0.62 else ((0.47 + rng.random() * 0.4799) if r < 0.92 else rng.random() * 0.469)
            score = round(score, 3)
            b = band(score)
            rec = {"id": f"D-{d}-{i:04d}", "claim": f"CW-26-{d:03d}{i:04d}", "day": d, "minute": minute, "doc": doc,
                   "passages": [f"CM-WL-07 v3 §{rng.randint(2, 9)}.{rng.randint(1, 6)}" for _ in range(3)],
                   "index": INDEX_ID, "model": MODEL_PIN, "score": score, "band": b, "router": ROUTER_ID,
                   "fields": out_fields, "fields_digest": digest(out_fields), "sent_prompt": sent,
                   "trace_input_tokens": tokens(sent) + doc["doc_tokens"]}
            if d < FIX:     # v0 run record: the prompt is named and the code commit is recorded, the text is not
                rec["prompt_ref"] = {"name": "intake-summary", "code_commit": COMMIT}
            else:           # v1 run record: the prompt is pinned by content and the gateway checks what it sent
                rec["prompt_ref"] = {"id": ID_B, "sent_sha": digest(sent)}
                rec["input_tokens"] = rec["trace_input_tokens"]
            if b != "proceed":
                lost = d == 188 and lost_n < 3 and i > 40
                lost_n += lost
                rec["review"] = None if lost else {"reviewer": f"A-{100 + rng.randint(1, 38)}", "outcome": rng.choices(
                    ["accepted", "edited"], [83, 17])[0], "seconds": rng.randint(40, 420)}
                rec["review_in_claims_core"] = {"reviewer": f"A-{100 + rng.randint(1, 38)}", "outcome": "accepted"}
            rec["action"] = {"ledger": f"AL-{digest(['al', d, i])[:8]}", "level": "draft", "target": "claims-core intake",
                             "verified": True}
            out.append(rec)
    return out


def disputed(recs):
    """The disputed claim: decided day 169, both addresses present, review band, reviewer accepted."""
    for r in recs:
        if r["day"] == 169 and r["doc"]["both"] and r["band"] == "review" and r.get("review", {}) and r["review"]["outcome"] == "accepted" and r["doc"]["doc_type"] == "FNOL form":
            return r
