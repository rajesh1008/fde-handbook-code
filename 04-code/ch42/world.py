"""Deterministic stand-in for Pennant's first ninety days in production (Chapter 42). Invented documents, invented
volumes; the calendar and the people follow the book's story calendar. Production day 0 = engagement day 168
[CHECK ch39/ch41]. No model calls: confidences and correctness are drawn from seeded generators."""
import random
import _paths  # noqa: F401

GO_LIVE = 168
CAL = dict(jenna_announced=9, jenna_last=14, rosa_holds=21, brf_change=19, grant_accepts=29, recal_signed=33,
           incident=38, review=40, runbook_change=43, notice=41, freeze=(45, 75), retire=62, account_moved=46,
           mr_approval=54, migrate=55, deputies=56, drill=70, live_stable=90)
TOP12 = ["BRF-INV", "HLS-BOL", "MAN-CONS", "CAR-A", "CAR-B", "CAR-C", "CAR-D", "CAR-E", "CAR-F", "CAR-G",
         "CAR-H", "CAR-I"]
SHARE = [0.14, 0.12, 0.06, 0.09, 0.08, 0.07, 0.07, 0.06, 0.05, 0.05, 0.04, 0.03]   # 76% in scope; rest to clerks
QUAL = dict(zip(TOP12, [0.90, 0.88, 0.80, 0.89, 0.88, 0.87, 0.89, 0.86, 0.88, 0.87, 0.86, 0.85]))
EU_SHARE = 0.18
THRESHOLD_V0 = 0.80


def volume(d):
    base = 2100 if d % 7 not in (5, 6) else 840
    return int(base * (1.6 if CAL["freeze"][0] <= d <= CAL["freeze"][1] else 1.0))


def mix(d):
    s = list(SHARE)
    if CAL["freeze"][0] <= d <= CAL["freeze"][1]:
        s[2] = 0.11; s[0] = 0.12; s[1] = 0.10   # peak season: more consolidated manifests
    return s


def day_docs(d, fixed=False):
    """One record per document in matcher scope: (layout, variant, confidence, correct, eu, fingerprint)."""
    r = random.Random(1000 + d)
    out = []
    n = volume(d)
    s = mix(d)
    for _ in range(n):
        x = r.random()
        acc, lay = 0.0, None
        for L, p in zip(TOP12, s):
            acc += p
            if x < acc:
                lay = L
                break
        if lay is None:
            continue                                 # out of scope (24%): clerks, as designed
        variant = "v2" if (lay == "BRF-INV" and d >= CAL["brf_change"]) else "v1"
        q = QUAL[lay]
        if variant == "v2" and not fixed:
            fp = min(0.99, max(0.4, r.gauss(0.74, 0.04)))   # the fingerprint still matches, at a lower score
            conf = min(0.99, max(0.3, r.gauss(q - 0.02, 0.06)))
            correct = r.random() < 0.80              # invoice total read from the new tax line: confident and wrong
        else:
            fp = min(0.99, max(0.4, r.gauss(0.95 if lay != "MAN-CONS" else 0.88, 0.02)))
            conf = min(0.99, max(0.3, r.gauss(q, 0.07)))
            correct = r.random() < (0.999 if conf >= 0.78 else 0.85)
        out.append((lay, variant, conf, correct, r.random() < EU_SHARE, fp))
    return out


def outcome(doc, t, route_layout=None):
    lay, var, c, ok, eu, fp = doc
    if c < t or (route_layout and (lay, var) == route_layout):
        return "route"
    return "matched" if ok else "silent"


def bins(xs, width=0.05):
    return [f"b{min(19, int(x / width))}" for x in xs]
