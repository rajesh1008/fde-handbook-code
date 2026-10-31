"""Deterministic stand-in for Chapter 25. No customer data and no model call anywhere in this folder.

ClaimsCore  a pre-production copy of a 2009-style claims system, reached through its first-notice screens:
            FNOL-1 assigns a claim number at once (a shell), FNOL-2 runs the business rules; a response can be lost
            after the claim is already committed (the screen times out on the confirmation page).
documents   first-notice documents with gold fields, the agent's proposed payload (with seeded extraction
            errors), a confidence, and the model's own one-line description of what it is about to write.
"""
import random

FIELDS = ("policy_no", "claimant", "loss_date", "loss_type", "cause_code", "zip")
FIRST = ["Emily", "Robert", "Maria", "James", "Linda", "David", "Susan", "Kevin", "Grace", "Omar", "Julia", "Henry"]
LAST = ["Carter", "Hayes", "Lopez", "Nguyen", "Brooks", "Patel", "Murphy", "Sullivan", "Reed", "Coleman", "Ortiz"]
TYPES = [("WATER", "WTR-01"), ("WATER", "WTR-02"), ("AUTO", "COL-01"), ("AUTO", "COL-02"), ("FIRE", "FIR-01"),
         ("THEFT", "THF-01"), ("WIND", "WND-01")]


def documents(n, day, seed, start=0):
    rng = random.Random(seed)
    docs = []
    for i in range(start, start + n):
        lt, cc = rng.choice(TYPES)
        m, d = rng.randint(1, 9), rng.randint(1, 28)
        gold = dict(policy_no=f"CM-{rng.randint(100000, 999999)}", claimant=f"{rng.choice(FIRST)} {rng.choice(LAST)}",
                    loss_date=f"2026-{m:02d}-{d:02d}", loss_type=lt, cause_code=cc, zip=f"06{rng.randint(100, 999)}")
        if lt == "WATER" and rng.random() < 0.025:
            gold["cause_code"] = ""                     # the document does not state a cause: V-118 will reject
        kind = "fnol" if rng.random() > 0.04 else "supporting"   # a supporting document for an existing claim
        pay, err = dict(gold), None
        r = rng.random()
        if r < 0.13:                                     # one seeded extraction error
            err = rng.choice(["loss_date", "loss_date", "zip", "cause_code", "claimant", "policy_no"])
            if err == "loss_date":
                pay[err] = f"2026-{d:02d}-{m:02d}" if d <= 12 and d != m else f"2026-{m:02d}-{min(d + 10, 28):02d}"
            elif err == "zip":
                pay[err] = gold["zip"][:-1] + str((int(gold["zip"][-1]) + 3) % 10)
            elif err == "cause_code":
                pay[err] = "WTR-02" if gold["cause_code"] != "WTR-02" else "WTR-01"
            elif err == "claimant":
                pay[err] = gold["claimant"].split()[0]
            else:
                pay[err] = gold["policy_no"][:-2] + gold["policy_no"][-1] + gold["policy_no"][-2]
            if pay[err] == gold[err]:
                err = None
        conf = round(min(0.99, max(0.30, (0.62 if err else 0.86) + rng.gauss(0, 0.11))), 2)
        said, q = dict(pay), rng.random()
        if err and q < 0.12:                             # the description reads right, the payload is wrong
            said[err] = gold[err]
        elif not err and q < 0.01:                       # the description is wrong, the payload is right
            said["loss_date"] = f"2026-{m:02d}-{min(d + 1, 28):02d}"
        narrative = f"Create claim for {said['claimant']}, policy {said['policy_no']}, loss {said['loss_date']}."
        docs.append(dict(doc_id=f"FN{day}-{i:04d}", day=day, kind=kind, gold=gold, payload=pay, error=err,
                         conf=conf, narrative=narrative, said=said))
    return docs


class ClaimsCore:
    """Pre-production claims-core. Rules on FNOL-2: V-118 a water loss needs a cause code."""

    def __init__(self, lose=None, start=3100):
        self.claims, self.n, self.lose = {}, start, dict(lose or {})   # lose: doc_id -> responses still to lose
        self.touched = set()

    def find(self, key):
        return next((c for c, r in self.claims.items() if r["agent_ref"] == key and r["status"] == "OPEN"), None)

    def write(self, rec, key):
        self.n += 1
        cid = f"CC-2026{self.n:04d}"
        self.claims[cid] = dict(rec, agent_ref=key, status="SHELL")       # FNOL-1 commits the number at once
        if rec["loss_type"] == "WATER" and not rec["cause_code"]:
            return False, cid, "V-118 water loss needs a cause code"
        self.claims[cid]["status"] = "OPEN"
        if self.lose.get(rec["doc_id"], 0) > 0:
            self.lose[rec["doc_id"]] -= 1
            raise TimeoutError("confirmation page timed out")
        return True, cid, ""

    def readback(self, cid):
        return self.claims[cid]

    def void(self, cid, reason="VOID-DUP"):
        if self.claims[cid]["status"] not in ("OPEN", "SHELL"):
            return False
        self.claims[cid]["status"] = reason if self.claims[cid]["status"] == "OPEN" else "VOID"
        return True

    def extract(self):
        return [dict(r, claim=c) for c, r in self.claims.items() if r["status"] == "OPEN"]
