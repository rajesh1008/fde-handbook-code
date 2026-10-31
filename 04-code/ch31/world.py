"""Chapter 31 deterministic stand-in for Caldwell Mutual's claims intake in the pilot configuration (rc-1).

Nothing here is Caldwell data. Every document, outcome and timing is drawn from a sha256 of its key, so every run
prints the same numbers. The totals that the book reports (84.0% on gold-heldout, 88.0% shadow agreement, 1.1%
post-review error) are parameters of this stand-in, set from the Blueprint scoreboard; the lab shows how each
number is computed and what moves it, not that a real system produced it.

Story calendar used here: shadow run on ten intake days, days 142 to 146 and 149 to 153; the orientation change
merges through the gate on day 150; router v1.1 (floor 0.47) on day 151 (Chapter 27); audit days 154 and 155;
Anne Kessler's scorecard day 156; the Shadow Exit gate belongs to Chapter 39."""
import hashlib
import _paths  # noqa: F401

FIELDS = ("policy_number", "claimant_name", "loss_date", "date_received", "loss_type", "loss_location",
          "injury_reported", "police_report_ref", "other_party", "intake_channel")
CRITICAL = ("policy_number", "loss_date", "loss_type")
SIX = ("policy number", "claimant", "loss date", "loss type", "cause code", "ZIP code")
STRATA = ("first notice, email", "first notice, fax", "first notice, mail", "police report", "repair estimate",
          "medical bill", "adjuster note", "photo log")
GOLD_CYCLE = list(STRATA) + ["first notice, fax", "first notice, mail"] * 2
FIELD_ADJ = dict(policy_number=0.03, claimant_name=0.03, loss_date=0.01, date_received=0.04, loss_type=-0.04,
                 loss_location=-0.06, injury_reported=0.0, police_report_ref=0.02, other_party=-0.07,
                 intake_channel=0.06)
BUILDS = ("p7 (day 94)", "rc-1 (day 156)")
RATE = {"p7 (day 94)": dict(zip(STRATA, (0.90, 0.60, 0.66, 0.84, 0.83, 0.82, 0.80, 0.79))),
        "rc-1 (day 156)": dict(zip(STRATA, (0.95, 0.72, 0.77, 0.89, 0.88, 0.87, 0.86, 0.85)))}
GOLD_CORRECT = {"p7 (day 94)": 1542, "rc-1 (day 156)": 1689}   # of 2,010 fields (Ch26: 76.7%; Blueprint: 84%)
GOLD_DOCS = 201

SHADOW_DAYS = (142, 143, 144, 145, 146, 149, 150, 151, 152, 153)
PER_DAY = 241
AGREE = (215, 209, 208, 206, 209, 212, 213, 216, 217, 216)      # documents agreeing on all six fields
FIX_DAY = 150            # orientation detection and the legibility gate merge through the pyramid gate
ROUTER_V11_DAY = 151     # Chapter 27: floor 0.41 -> 0.47, signed by Anne Kessler
TEMPLATE = {143: 5, 144: 6, 145: 7, 146: 7, 149: 7, 150: 6}     # broker template change day 143 (Chapter 27)
ROTATED_PRE, ROTATED_POST = 13, 6
CAUSES = (("rotated fax, no intake record", None), ("broker template, date received", None),
          ("other agent error", 125), ("clerk keying error, agent right", 52), ("equivalent format", 61))
CHANNELS = (("email", 0.44), ("fax", 0.22), ("mail scan", 0.24), ("agency portal", 0.10))
BANDS = dict(escalate=189, review=714)          # of routed documents; the rest proceed
AUDIT = dict(pre=(240, 32), post=(160, 12))      # audit-shadow-400: documents and post-review field errors

RELEASE = dict(name="rc-1", extractor="p8.3", pin="extract-2026-04", c06="c06-p4", c07="c07-small-2",
               router="v1.1 (proceed 0.95, floor 0.47)", guardrails="cw-rules v1 (8 cards)",
               index="claims manual index, CM-WL-07 v3 current", boundary="release boundary v2 (day 118)",
               gate="pyramid, Caldwell CI under nl-eval")


def u(*key):
    h = hashlib.sha256("|".join(map(str, key)).encode()).hexdigest()
    return int(h[:12], 16) / 16 ** 12


def pick(keys, k, *salt):
    return sorted(keys, key=lambda x: u(*salt, x))[:k]


def allocate(sizes, rates, total):
    """Integer counts per cell, proportional to size x rate, capped at size, summing exactly to total."""
    raw = {k: sizes[k] * rates[k] for k in sizes}
    scale = total / sum(raw.values())
    exact = {k: min(sizes[k], raw[k] * scale) for k in sizes}
    base = {k: int(v) for k, v in exact.items()}
    left, order, i = total - sum(base.values()), sorted(sizes, key=lambda k: (-(exact[k] - int(exact[k])), str(k))), 0
    while left > 0:
        k = order[i % len(order)]
        if base[k] < sizes[k]:
            base[k] += 1; left -= 1
        i += 1
    return base


def gold_docs():
    return [(f"G-{i:03d}", GOLD_CYCLE[i % len(GOLD_CYCLE)]) for i in range(GOLD_DOCS)]


def gold_scores(build):
    """{(doc, field): correct} for one build on gold-heldout (201 documents, 2,010 fields)."""
    docs = gold_docs()
    sizes = {(s, f): sum(1 for _, t in docs if t == s) for s in STRATA for f in FIELDS}
    rates = {(s, f): min(0.995, RATE[build][s] + FIELD_ADJ[f]) for s, f in sizes}
    quota = allocate(sizes, rates, GOLD_CORRECT[build])
    out = {}
    for (s, f), k in quota.items():
        ids = [d for d, t in docs if t == s]
        good = set(pick(ids, k, build, f))
        for d in ids:
            out[(d, f)] = d in good
    return out


def channel(doc_id):
    x, acc = u("channel", doc_id), 0.0
    for name, share in CHANNELS:
        acc += share
        if x < acc:
            return name
    return CHANNELS[-1][0]


def shadow_docs():
    return [dict(id=f"S{d}-{i:03d}", day=d, channel=channel(f"S{d}-{i:03d}"))
            for d in SHADOW_DAYS for i in range(PER_DAY)]


def shadow():
    """Every shadow document with its rotation, agreement, disagreement cause and band."""
    docs = shadow_docs()
    fax_pre = [x["id"] for x in docs if x["channel"] == "fax" and x["day"] < FIX_DAY]
    fax_post = [x["id"] for x in docs if x["channel"] == "fax" and x["day"] >= FIX_DAY]
    rot_pre, rot_post = set(pick(fax_pre, ROTATED_PRE, "rot")), set(pick(fax_post, ROTATED_POST, "rot"))
    fnol_rot = set(pick(sorted(rot_pre), 9, "fnol"))          # 9 first notices, 4 repair estimates
    rest_pool = []
    for i, d in enumerate(SHADOW_DAYS):
        day = [x for x in docs if x["day"] == d]
        n_dis = PER_DAY - AGREE[i]
        for x in day:
            x["rotated"] = x["id"] in rot_pre or x["id"] in rot_post
            x["kind"] = ("first notice" if x["id"] in fnol_rot else "repair estimate") if x["id"] in rot_pre else ""
            x["agree"], x["cause"] = True, ""
        forced = [x for x in day if x["id"] in rot_pre]
        for x in forced:
            x["agree"], x["cause"] = False, CAUSES[0][0]
        free = [x["id"] for x in day if x["id"] not in rot_pre]
        drift = set(pick(free, TEMPLATE.get(d, 0), "drift"))
        for x in day:
            if x["id"] in drift:
                x["agree"], x["cause"] = False, CAUSES[1][0]
        free = [i_ for i_ in free if i_ not in drift]
        more = set(pick(free, n_dis - len(forced) - len(drift), "dis"))
        for x in day:
            if x["id"] in more:
                x["agree"] = False
                rest_pool.append(x)
    rest_pool.sort(key=lambda x: u("cause", x["id"]))
    j = 0
    for name, n in CAUSES[2:]:
        for x in rest_pool[j:j + n]:
            x["cause"] = name
        j += n
    assert j == len(rest_pool), (j, len(rest_pool))
    routed = [x for x in docs if x["id"] not in rot_pre]
    lean = {"other agent error": 0.35, "broker template, date received": 0.25}
    routed.sort(key=lambda x: u("band", x["id"]) - lean.get(x["cause"], 0.0))
    for k, x in enumerate(routed):
        x["band"] = "escalate" if k < BANDS["escalate"] else "review" if k < BANDS["escalate"] + BANDS["review"] else "proceed"
    for x in docs:
        x.setdefault("band", "none: correspondence queue")
    return docs
