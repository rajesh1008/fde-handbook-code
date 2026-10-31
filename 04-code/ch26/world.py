"""Deterministic stand-in for Caldwell's gold set (Chapter 26). Not Caldwell data.

300 documents drawn to the Chapter 16 plan (eight strata, fax and mail first notices oversampled, a floor of 20),
ten fields each. For every field the stand-in fixes four facts, from hashed uniforms so every run is identical:
  nl_ok      the extractor (extract-2026-04, prompt p6) matches the value as Northlight's evaluation set defines it
  defdiff    Caldwell's definition of the field gives a different value on this document (stamp date, cause code...)
  plausible  when the extractor is wrong, the wrong value looks reasonable on the page
  conf       the extractor's own confidence
Anne Kessler's adjusters score a field correct only if it matches Caldwell's definition: nl_ok and not defdiff.
Two judges stand in for model judges: judge_v1 is Northlight's reference-free judge with Northlight's rubric
(the injected failure: it agrees with the model and disagrees with Anne); judge_v2 has Caldwell's rubric."""
import hashlib
import _paths  # noqa: F401
from fieldkit.sampling import allocate

FIELDS = ["policy_number", "claimant_name", "loss_date", "date_received", "loss_type", "loss_location",
          "injury_reported", "police_report_ref", "other_party", "intake_channel"]
JUDGMENT = {"claimant_name", "loss_location", "other_party"}
EXACT = set(FIELDS) - JUDGMENT
CRITICAL = ("policy_number", "loss_date", "loss_type")          # the fields that route a claim
POP = {"medical bill": 2485, "adjuster note": 2343, "photo log": 2343, "police report": 2130,
       "repair estimate": 1917, "first notice, email": 1633, "first notice, fax": 923, "first notice, mail": 426}
# the draw Kessler signed on day 59 (Chapter 16, Listing 16.x): drawn count and weight per stratum
_plan = allocate(POP, 300, floor=20, oversample={"first notice, fax": 1.5, "first notice, mail": 1.5})
PLAN = {"medical bill": (44, 1.19), "adjuster note": (44, 1.12), "photo log": (45, 1.10),
        "police report": (44, 1.02), "repair estimate": (40, 1.01), "first notice, email": (34, 1.01),
        "first notice, fax": (29, 0.67), "first notice, mail": (20, 0.45)}
BASE_ERR = {"medical bill": .090, "adjuster note": .110, "photo log": .120, "police report": .080,
            "repair estimate": .100, "first notice, email": .070, "first notice, fax": .200, "first notice, mail": .240}
MULT = dict(policy_number=.6, claimant_name=.8, loss_date=1.0, date_received=1.2, loss_type=1.0, loss_location=1.3,
            injury_reported=.8, police_report_ref=1.2, other_party=1.4, intake_channel=.4)
DEF = dict(loss_type=.40, loss_location=.24, injury_reported=.29, other_party=.14)
DATE_DEF = {"first notice, mail": .75, "first notice, fax": .35, "first notice, email": .05}


def u(*k):
    return int(hashlib.sha256("|".join(map(str, k)).encode()).hexdigest()[:12], 16) / 16 ** 12


def defdiff_p(s, f):
    if f == "date_received":
        return DATE_DEF.get(s, .35)
    return DEF.get(f, 0.0)


class Item:
    __slots__ = ("doc", "field", "stratum", "weight", "nl_ok", "defdiff", "plausible", "conf", "split", "age")

    def __init__(self, doc, f, s, w, split, age, err_scale=1.0, caldwell=True):
        self.doc, self.field, self.stratum, self.weight, self.split, self.age = doc, f, s, w, split, age
        self.nl_ok = u(doc, f, "nl") >= min(.9, BASE_ERR[s] * MULT[f] * err_scale * 2.0)
        self.defdiff = caldwell and u(doc, f, "def") < defdiff_p(s, f)
        self.plausible = u(doc, f, "kind") < .6
        r = u(doc, f, "conf")
        if self.nl_ok and self.defdiff:
            self.conf = .80 + .20 * r                       # confidently right by the wrong definition
        elif self.nl_ok:
            self.conf = .55 + .45 * r ** .35
        else:
            self.conf = .25 + .55 * r
    @property
    def key(self): return (self.doc, self.field)
    @property
    def anne_ok(self): return self.nl_ok and not self.defdiff


def gold_docs():
    docs, i = [], 0
    for s in sorted(PLAN, key=lambda s: -POP[s]):
        n, w = PLAN[s]
        for _ in range(n):
            d = f"G{i:03d}"
            docs.append((d, s, w, "dev" if u(d, "split") < 1 / 3 else "test", int(u(d, "age") * 60)))
            i += 1
    return docs


def gold_items():
    return [Item(d, f, s, w, sp, age) for d, s, w, sp, age in gold_docs() for f in FIELDS]


def northlight_items():
    """Northlight's own evaluation cases: the 200 development documents and 100 synthetic edge cases."""
    out, strata = [], list(POP)
    for i in range(300):
        s = strata[int(u("nlcase", i, "s") * len(strata))]
        scale = .56 if i < 200 else .46
        out.append([Item(f"N{i:03d}", f, s, 1.0, "nl", 99, err_scale=scale, caldwell=False) for f in FIELDS])
    return [it for doc in out for it in doc]


def judge_v1(it, run=0):
    """Reference-free, Northlight's rubric, sees only the page and the model's answer."""
    p = .985 if it.nl_ok else (.50 if it.plausible else .10)
    return u(it.doc, it.field, "j1", run) < p


def judge_v2(it, run=0):
    """Caldwell's rubric (Anne's definitions and eight adjudicated examples), still reference-free."""
    if it.anne_ok:
        p = .965
    elif it.nl_ok:            # right by Northlight's definition, wrong by Caldwell's
        p = .10
    else:
        p = .22 if it.plausible else .04
    # pinned version at temperature 0: most verdicts repeat; the rest are fresh draws
    draw = u(it.doc, it.field, "j2", 0) if u(it.doc, it.field, "j2stick", run) < .92 else u(it.doc, it.field, "j2", run)
    return draw < p


FIX = dict(date_received=.80, loss_type=.55, injury_reported=.85, loss_location=.60, other_party=.50)


def candidate(it, name):
    """Anne-correctness of a field under a candidate change."""
    ok = it.anne_ok
    if name in ("p7", "p7+alias"):
        if it.nl_ok and it.defdiff and u(it.doc, it.field, "fix") < FIX.get(it.field, 0):
            ok = True
        elif ok and u(it.doc, it.field, "break") < .006:
            ok = False
        elif not it.nl_ok and u(it.doc, it.field, "fix2") < .08:
            ok = True
    if name == "p7+alias":
        if not ok and not it.defdiff and u(it.doc, it.field, "alias+") < .30:
            ok = True
        elif ok and it.field == "policy_number" and it.stratum.endswith(("fax", "mail")) \
                and u(it.doc, it.field, "alias-") < .14:
            ok = False
        elif ok and it.field == "loss_date" and u(it.doc, it.field, "alias-") < .010:
            ok = False
    return ok


def weighted_acc(items, ok=lambda it: it.anne_ok):
    num = sum(it.weight for it in items if ok(it))
    return num / sum(it.weight for it in items)


def acc(items, ok=lambda it: it.anne_ok):
    return sum(1 for it in items if ok(it)) / len(items)
