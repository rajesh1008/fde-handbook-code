"""Chapter 39 world. Deterministic stand-in: seeded generators, no model calls, no customer data.

Caldwell: the shadow window of Chapter 31 (intake days 142 to 146 and 149 to 153, 241 documents a day),
reproduced document by document so that every total matches Listing 31.x: 2,410 documents, 2,121
agreements, 289 disagreements in five adjudicated causes, routing 1,494 / 714 / 189 / 13 untyped.
Greystone: a 20 clinic-day shadow of prior-authorization drafts beginning on Greystone's day 131,
with a holiday week on clinic days 11 to 15 (stand-in; ledgered)."""
import random
import _paths  # noqa: F401
from fieldkit.evals import wilson

STRATA = ("first notice, email", "first notice, fax", "first notice, mail", "police report",
          "repair estimate", "medical bill", "adjuster note", "photo log")
REFERENCE = dict(zip(STRATA, (0.24, 0.12, 0.14, 0.08, 0.14, 0.12, 0.09, 0.07)))  # reference-month mix
DIFFICULTY = dict(zip(STRATA, (0.05, 0.22, 0.19, 0.10, 0.10, 0.11, 0.12, 0.13)))  # weights for agent errors
DAYS = (142, 143, 144, 145, 146, 149, 150, 151, 152, 153)
PER_DAY = 241
AGREE = dict(zip(DAYS, (215, 209, 208, 206, 209, 212, 213, 216, 217, 216)))
ROTATED = dict(zip(DAYS, (2, 4, 2, 1, 0, 4, 0, 1, 3, 2)))
TEMPLATE = dict(zip(DAYS, (0, 5, 6, 7, 7, 7, 6, 0, 0, 0)))
ORIENTATION_FIX, TEMPLATE_FIX, ROUTER_V11 = 150, 151, 151
CHANGES = [(150, "orientation fix", ("first notice, fax",)),
           (151, "broker-template date rule", ("first notice, email",)),
           (151, "router v1.1 (proceed 0.95, floor 0.47)", ())]  # routing only: touches bands, not values
CAUSES = {"equivalent format": 61, "clerk keying error, agent right": 52, "other agent error": 125}
BANDS = {  # band totals per cause over the window; agreements carry the rest
    "broker template, date received": {"proceed": 19, "review": 19},
    "other agent error": {"proceed": 22, "review": 63, "escalate": 40},
    "equivalent format": {"proceed": 35, "review": 20, "escalate": 6},
    "clerk keying error, agent right": {"proceed": 30, "review": 18, "escalate": 4},
    "agree": {"proceed": 1388, "review": 594, "escalate": 139}}
STREAMS = ("schema and type", "business rules", "system of record", "source grounding",
           "second extraction", "cross-document")
STREAM_P = (0.12, 0.20, 0.30, 0.34, 0.42, 0.10)
AGENT_WRONG = ("other agent error", "broker template, date received", "rotated fax, no intake record")


def _counts(mix, n, rng, jitter=0):
    raw = {s: mix[s] * n for s in STRATA}
    c = {s: int(raw[s]) for s in STRATA}
    for s in sorted(STRATA, key=lambda s: raw[s] - c[s], reverse=True)[: n - sum(c.values())]:
        c[s] += 1
    for _ in range(jitter):
        a, b = rng.sample(STRATA, 2)
        if c[a] > 3:
            c[a] -= 1; c[b] += 1
    return c


def _cum_split(totals, rows):
    """Split column totals across rows with row sums fixed (cumulative rounding)."""
    keys = list(totals); out = {r: {} for r in rows}; R = sum(rows.values()); cum = 0
    prev = {k: 0 for k in keys}
    for r, n in rows.items():
        cum += n
        for k in keys[:-1]:
            t = round(totals[k] * cum / R); out[r][k] = t - prev[k]; prev[k] = t
        out[r][keys[-1]] = n - sum(out[r][k] for k in keys[:-1])
    return out


def caldwell_window():
    """Every shadow document: dict(day, id, stratum, cause|None, band, streams tuple, wrong, silent)."""
    rem = {d: PER_DAY - AGREE[d] - (ROTATED[d] if d < ORIENTATION_FIX else 0) - TEMPLATE[d] for d in DAYS}
    split = _cum_split(dict(CAUSES), rem)
    docs = []
    for d in DAYS:
        rng = random.Random(3900 + d)
        c = _counts(REFERENCE, PER_DAY, rng, jitter=6)
        day = [dict(day=d, id=f"C{d}-{i:03d}", stratum=s, cause=None) for i, s in
               enumerate(s for s in STRATA for _ in range(c[s]))]
        rng.shuffle(day)
        fax = [x for x in day if x["stratum"] == "first notice, fax"]
        for x in fax[:ROTATED[d]]:
            x["rotated"] = True
            if d < ORIENTATION_FIX:
                x["cause"] = "rotated fax, no intake record"
        email = [x for x in day if x["stratum"] == "first notice, email" and x["cause"] is None]
        for x in email[:TEMPLATE[d]]:
            x["cause"] = "broker template, date received"
        for cause, k in split[d].items():
            pool = [x for x in day if x["cause"] is None]
            w = [DIFFICULTY[x["stratum"]] if cause == "other agent error" else 1.0 for x in pool]
            chosen = set()
            while len(chosen) < k:
                chosen.add(rng.choices(range(len(pool)), weights=w)[0])
            for i in chosen:
                pool[i]["cause"] = cause
        docs += day
    rng = random.Random(39)
    for cause, bands in BANDS.items():
        group = [x for x in docs if (x["cause"] or "agree") == cause]
        lab = [b for b, n in bands.items() for _ in range(n)]
        assert len(lab) == len(group), (cause, len(lab), len(group))
        rng.shuffle(lab)
        for x, b in zip(group, lab):
            x["band"] = b
    srng = random.Random(3939)
    for x in docs:
        if x["cause"] == "rotated fax, no intake record":
            x["band"] = "none"
        x["wrong"] = x["cause"] in AGENT_WRONG
        x["streams"] = ()
        if x["cause"] == "other agent error":
            x["streams"] = tuple(s for s, p in zip(STREAMS, STREAM_P) if srng.random() < p)
        x["silent"] = x["wrong"] and (x["band"] == "none" or (x["band"] == "proceed" and not x["streams"]))
    return docs


def agreement(docs):
    k = sum(1 for x in docs if x["cause"] is None); n = len(docs)
    lo, hi = wilson(k, n)
    return k, n, k / n, lo, hi


def by_stratum(docs):
    out = {}
    for s in STRATA:
        g = [x for x in docs if x["stratum"] == s]
        out[s] = (sum(1 for x in g if x["cause"] is None), len(g))
    return out


def mix_of(docs):
    n = len(docs)
    return {s: sum(1 for x in docs if x["stratum"] == s) / n for s in STRATA}


def tvd(a, b):
    return 0.5 * sum(abs(a[s] - b[s]) for s in STRATA)


def reweighted(per, mix=REFERENCE):
    return sum(mix[s] * (per[s][0] / per[s][1] if per[s][1] else 0.0) for s in STRATA)


# ---- the holiday-mix failure injection (replay of a year-end intake week through a build that regressed on paper)
HOLIDAY = dict(zip(STRATA, (0.50, 0.03, 0.04, 0.06, 0.12, 0.11, 0.08, 0.06)))
REGRESSION = {"first notice, fax": 0.52, "first notice, mail": 0.60}


def holiday_week(rates, days=(149, 150, 151, 152, 153), seed=3947):
    rng = random.Random(seed); docs = []
    for d in days:
        c = _counts(HOLIDAY, PER_DAY, rng, jitter=4)
        for s in STRATA:
            p = REGRESSION.get(s, rates[s])
            for i in range(c[s]):
                docs.append(dict(day=d, id=f"H{d}-{s[:4]}{i}", stratum=s,
                                 cause=None if rng.random() < p else "injected disagreement",
                                 band="review", wrong=False, silent=False, streams=()))
    return docs


# ---- Greystone: prior-authorization drafts in shadow (drafts never shown to coordinators)
G_CLASSES = ("no prior auth needed", "prior auth, standard payer form", "prior auth, portal criteria",
             "prior auth, medical-necessity letter")
G_REF = dict(zip(G_CLASSES, (0.46, 0.28, 0.16, 0.10)))
G_HOL = dict(zip(G_CLASSES, (0.78, 0.14, 0.06, 0.02)))
G_RATE = dict(zip(G_CLASSES, (0.97, 0.86, 0.74, 0.62)))
G_FLAG = dict(zip(G_CLASSES, (0.70, 0.62, 0.50, 0.40)))  # chance a rule or flag fires on a wrong draft
G_DAYS = tuple(range(1, 21)); G_HOLIDAY_DAYS = (11, 12, 13, 14, 15)


def greystone_window(seed=3931):
    rng = random.Random(seed); out = []
    for d in G_DAYS:
        hol = d in G_HOLIDAY_DAYS
        mix, n = (G_HOL, 12) if hol else (G_REF, 22)
        raw = {c: mix[c] * n for c in G_CLASSES}; cnt = {c: int(raw[c]) for c in G_CLASSES}
        for c in sorted(G_CLASSES, key=lambda c: raw[c] - cnt[c], reverse=True)[: n - sum(cnt.values())]:
            cnt[c] += 1
        for c in G_CLASSES:
            for i in range(cnt[c]):
                agree = rng.random() < G_RATE[c]
                flagged = (not agree) and rng.random() < G_FLAG[c]
                out.append(dict(day=d, cls=c, agree=agree, wrong=not agree, silent=(not agree) and not flagged))
    return out
