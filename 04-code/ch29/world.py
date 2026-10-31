"""Deterministic stand-in for the Caldwell claims-intake agent as the Chapter 29 pyramid sees it.

Nothing here is Caldwell data and there are no model calls. Every value comes from a hash of its key, so every run
prints the same numbers. Fields, critical fields and strata follow Chapters 26 and 27 (gold-set-300: 99 development,
201 held-out test documents, scored by Anne Kessler's adjusters). Prompt "p8.3" is the extractor prompt in Caldwell's
main branch on day 141; "p9" is pull request #212 (day 146), which adds three email examples and an instruction to
take the date received from the letter. Costs use a stand-in rate card, not Caldwell's contract prices.
"""
import hashlib
import _paths  # noqa: F401

FIELDS = ("policy_number", "claimant_name", "loss_date", "date_received", "loss_type", "loss_location",
          "injury_reported", "police_report_ref", "other_party", "intake_channel")
CRITICAL = ("policy_number", "loss_date", "loss_type")
SYSTEM_CHECKED = ("policy_number", "loss_date", "date_received", "intake_channel")
TWO_SOURCE_FIELDS = ("policy_number", "claimant_name", "loss_date")
STRATA_ACC = {"first notice, email": 0.972, "first notice, fax": 0.83, "first notice, mail": 0.86,
              "police report": 0.944, "repair estimate": 0.934, "medical bill": 0.924, "adjuster note": 0.924,
              "photo log": 0.914}
FIELD_ADJ = dict(policy_number=0.03, claimant_name=0.03, loss_date=0.01, date_received=0.04, loss_type=-0.04,
                 loss_location=-0.06, injury_reported=0.0, police_report_ref=0.02, other_party=-0.07, intake_channel=0.06)
GOLD_CYCLE = list(STRATA_ACC) + ["first notice, fax", "first notice, mail"] * 2
P9_LIFT = dict(loss_type=0.06, loss_location=0.08, other_party=0.08)

# stand-in rate card and timing model (labeled in every output that uses them)
RATE_IN, RATE_OUT = 3.00 / 1e6, 15.00 / 1e6          # dollars per token, stand-in
DOC_TOKENS_IN, DOC_TOKENS_OUT = 5200, 450
Q_TOKENS_IN, Q_TOKENS_OUT = 3000, 300
CALL_SECONDS, CONCURRENCY = 7.5, 8


def u(*key) -> float:
    h = hashlib.sha256("|".join(map(str, key)).encode()).hexdigest()
    return int(h[:12], 16) / 16 ** 12


def doc_cost(passes=2):
    return passes * (DOC_TOKENS_IN * RATE_IN + DOC_TOKENS_OUT * RATE_OUT)


def q_cost():
    return Q_TOKENS_IN * RATE_IN + Q_TOKENS_OUT * RATE_OUT


def gold_test():
    return [(f"GT-{i + 1:04d}", GOLD_CYCLE[i % len(GOLD_CYCLE)]) for i in range(201)]


def p_right(prompt, stratum, field):
    p = STRATA_ACC[stratum] + FIELD_ADJ[field]
    if prompt == "p9":
        p += P9_LIFT.get(field, 0.0) * (0.5 if stratum == "first notice, mail" else 1.0)
        if stratum == "first notice, mail" and field == "date_received":
            p = 0.30          # the letter's date, not the mailroom stamp (Chapter 8 ruling)
    return max(0.02, min(0.995, p))


def extract(prompt, docs=None):
    docs = docs or gold_test()
    return {(d, f): u(d, f, "draw") < p_right(prompt, s, f) for d, s in docs for f in FIELDS}


STRATUM = dict(gold_test())

# --------------------------------------------------------------------------------------------- layer one: rules
FAMILIES = {"date normalization": 96, "policy number format": 48, "V-118 cause code": 72,
            "prompt-payment deadline": 60, "intent key": 44, "permission filter": 36, "router gates": 32,
            "budget breaker": 24}


def rule_cases():
    cases = []
    for fam, n in FAMILIES.items():
        for i in range(n):
            m, d = 1 + int(u(fam, i, "m") * 12), 1 + int(u(fam, i, "d") * 28)
            cases.append(dict(family=fam, i=i, date=f"{m:02d}/{d:02d}/20{24 + int(u(fam, i, 'y') * 3)}",
                              m=m, d=d, dated=fam in ("date normalization", "prompt-payment deadline")))
    return cases


def parse_date(s, datelib):
    """datelib 3.9 reads month first; 4.0 changed the default to day first when both parts are 12 or less."""
    a, b, y = (int(x) for x in s.split("/"))
    if datelib >= 4.0 and a <= 12 and b <= 12:
        a, b = b, a
    return (y, a, b)


# ------------------------------------------------------------------------------- component: retrieval answers
QTYPES = {"procedure": 62, "form or code": 28, "version-sensitive": 24, "cross-document": 21, "not in the documents": 15}


def questions():
    out = []
    for t, n in QTYPES.items():
        out += [(f"AQ-{len(out) + i + 1:03d}", t) for i in range(n)]
    return out


def answer_claims(qid, qtype, lifecycle=True):
    """Claims in the assistant's answer; each is (claim id, supported by the cited current passage?, cites
    superseded?). Without the lifecycle filter a version-sensitive answer cites the superseded wording."""
    if qtype == "not in the documents":
        return []
    k = 1 + int(u(qid, "nclaims") * 4)
    out = []
    for c in range(k):
        sup = u(qid, c, "sup") < 0.975
        sup_ver = (not lifecycle) and qtype == "version-sensitive" and c == 0
        out.append((f"{qid}.{c}", sup and not sup_ver, sup_ver))
    return out


def checker_flags(cid, supported):
    """Stand-in faithfulness checker: compares each claim to its cited passage. Catches most unsupported claims,
    raises a few false alarms."""
    r = u(cid, "chk")
    return (r < 0.92) if not supported else (r < 0.03)
