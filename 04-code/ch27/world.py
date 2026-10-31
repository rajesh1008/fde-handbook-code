"""Deterministic stand-in for Caldwell's first-notice documents as the Chapter 27 router sees them.

Nothing here is Caldwell data and there are no model calls. Every value comes from a hash of (set, document, field,
purpose), so every run prints the same numbers. The shape is chosen to match the book's story: a verbalized
confidence that is calibrated on Northlight's synthetic set and inflated on real documents, errors that cluster in
poor documents (fax and mail), and deterministic evidence (the value appears in the source, claims-core agrees,
two sources agree) plus a second extraction pass that separate right from wrong far better than the model's own number.

Fields and strata follow Chapter 26 (gold-set-300). Sets:
  synthetic-2000   Northlight's synthetic set from Chapter 16 (what router v0 was calibrated on, day 120)
  gold-heldout     the 201 held-out documents of gold-set-300 (Chapter 26), first real sample for router v0
  cal-600          600 shadow documents scored by Anne Kessler's adjusters, days 124 to 131
  audit-400        400 documents worked through routed review, days 136 to 139, audited by Anne's team
  week-N           weekly drift samples (Chapter 27 drift rehearsal)
"""
import hashlib
import math
import _paths  # noqa: F401
from fieldkit.routing import Evidence

FIELDS = ("policy_number", "claimant_name", "loss_date", "date_received", "loss_type", "loss_location",
          "injury_reported", "police_report_ref", "other_party", "intake_channel")
CRITICAL = ("policy_number", "loss_date", "loss_type")
FIELD_BIAS = dict(policy_number=0.6, claimant_name=0.5, loss_date=0.4, date_received=-0.2, loss_type=-0.3,
                  loss_location=-0.5, injury_reported=0.0, police_report_ref=0.5, other_party=-0.6, intake_channel=1.2)
SYSTEM_CHECKED = ("policy_number", "loss_date", "date_received", "intake_channel")   # claims-core, V-127, mail log
TWO_SOURCE_FIELDS = ("policy_number", "claimant_name", "loss_date")
# stratum: (share of the month, share of medium documents, share of hard documents). Errors cluster: a clean
# document is almost always right, a medium one (skewed scan, handwriting in one box) is right about seven fields
# in ten, a hard one (a faxed fax, a photo of a form) is mostly wrong.
STRATA = {"first notice, email": (0.24, 0.15, 0.01), "first notice, fax": (0.12, 0.44, 0.14),
          "first notice, mail": (0.08, 0.42, 0.12), "police report": (0.12, 0.23, 0.02),
          "repair estimate": (0.12, 0.24, 0.02), "medical bill": (0.11, 0.25, 0.03),
          "adjuster note": (0.11, 0.25, 0.03), "photo log": (0.10, 0.27, 0.03)}
GOLD_CYCLE = list(STRATA) + ["first notice, fax", "first notice, mail"] * 2   # Chapter 16 plan: fax and mail oversampled
VERBAL = (0.6, 0.7, 0.8, 0.9, 0.95, 0.99)
P = dict(A=-0.1, B=13.8, found_wrong=0.99, sys_wrong=0.35, rerun_wrong=0.85, med_lo=0.50, fill_in=0.03)


def u(*key) -> float:
    h = hashlib.sha256("|".join(map(str, key)).encode()).hexdigest()
    return int(h[:12], 16) / 16 ** 12


def sig(z):
    return 1 / (1 + math.exp(-z))


def quantize(x):
    return min(VERBAL, key=lambda v: abs(v - x))


class Item:
    __slots__ = ("set", "doc", "field", "stratum", "q", "right", "verbal", "ev", "two_source", "rerun", "tmpl2")

    def features(self, v2=False):
        sc = self.ev.system_check
        return [math.log(self.verbal / (1 - self.verbal)), 1.0 if self.ev.found_in_source else 0.0,
                1.0 if sc is True else 0.0, 1.0 if sc is False else 0.0, self.q,
                1.0 if self.rerun else 0.0,
                ] + [1.0 if self.field == f else 0.0 for f in FIELDS[1:]] + \
            ([1.0 if self.tmpl2 and self.field in DATE_FIELDS else 0.0] if v2 else [])


DATE_FIELDS = ("loss_date", "date_received")
FEATURE_NAMES = ("verbal logit", "found in source", "system check passed", "system check failed", "quality",
                 "second pass agrees") + \
    tuple(f"field={f}" for f in FIELDS[1:])


def _stratum(s, d):
    r, acc = u(s, d, "stratum"), 0.0
    for name, (share, _, _) in STRATA.items():
        acc += share
        if r < acc:
            return name
    return name


def make(setname, n_docs, synthetic=False, shift=None, stratified=False, template=None, only=None):
    """shift: optional dict(stratum=..., extra_medium=..., extra_hard=...) moves the document mix.
    template: optional dict(stratum=..., share=..., wrong=...) for the drift rehearsal: one broker's new form puts
    the date reported where the loss date used to be, so the date fields come out wrong on clean documents with every
    piece of evidence passing (the value is in the source, the date is plausible, a second pass reads it the same).
    only: draw every document from this stratum (the recalibration sample)."""
    items = []
    for i in range(n_docs):
        d = f"{setname[:3].upper()}-{i:04d}"
        st = only or (GOLD_CYCLE[i % len(GOLD_CYCLE)] if stratified else _stratum(setname, d))
        share, med, hard = STRATA[st]
        if shift and st == shift["stratum"]:
            med, hard = med + shift["extra_medium"], hard + shift["extra_hard"]
        r = u(setname, d, "tier")
        if synthetic:
            q = 0.80 + 0.18 * u(setname, d, "q")
        elif r < hard:
            q = 0.30 + 0.15 * u(setname, d, "q")
        elif r < hard + med:
            q = P["med_lo"] + 0.20 * u(setname, d, "q")
        else:
            q = 0.80 + 0.18 * u(setname, d, "q")
        two = st == "first notice, email" and u(setname, d, "two") < 0.55
        budget_ok = u(setname, d, "budget") > 0.006
        t2 = bool(template and st == template["stratum"] and u(setname, d, "tmpl") < template["share"])
        for f in FIELDS:
            it = Item()
            it.set, it.doc, it.field, it.stratum, it.q, it.two_source = setname, d, f, st, q, two
            if synthetic:
                v = quantize(0.62 + 0.38 * u(setname, d, f, "v") ** 0.45)
                it.right = u(setname, d, f, "right") < v - 0.004
            else:
                p = sig(P["A"] + P["B"] * (q - 0.5) + FIELD_BIAS[f])
                it.right = u(setname, d, f, "right") < p
                v = quantize(0.95 + 0.01 * it.right + P["fill_in"] * (q < 0.75) + 0.07 * (u(setname, d, f, "v") - 0.5))
            it.verbal = v
            r = it.right
            found = u(setname, d, f, "found") < (0.999 if r else P["found_wrong"])
            sc = None
            if f in SYSTEM_CHECKED:
                sc = u(setname, d, f, "sys") < (0.996 if r else P["sys_wrong"])
            agree = None
            if two and f in TWO_SOURCE_FIELDS:
                agree = u(setname, d, f, "agree") < (0.995 if r else 0.45)
            it.rerun = u(setname, d, f, "rerun") < (0.99 if r else P["rerun_wrong"])
            it.ev = Evidence(found, sc, agree, budget_ok)
            it.tmpl2 = t2
            if t2 and f in DATE_FIELDS and u(setname, d, f, "tmpl") < template["wrong"]:
                it.right, it.rerun = False, True
                it.ev = Evidence(True, True if f in SYSTEM_CHECKED else None, None, budget_ok)
            items.append(it)
    return items


def docs(items):
    out = {}
    for it in items:
        out.setdefault(it.doc, []).append(it)
    return out


# reviewer behavior in routed review (stand-in rates, Chapter 25's review surface)
SCRATCH = dict(clean=0.004, medium=0.012, hard=0.03)   # error rate keying a field from the source, no suggestion
MISS = dict(clean=0.06, medium=0.06, hard=0.25)        # share of wrong suggestions a reviewer accepts


def tier(q):
    return "hard" if q < 0.46 else ("medium" if q < 0.80 else "clean")


def review_outcome(it, band, shown=True):
    """Return True if the final value after the human step is right.
    proceed: nobody looks. review with a suggestion shown: the reviewer confirms or corrects it, and on an
    illegible document tends to accept a plausible wrong value. No suggestion (escalated, or below the floor):
    the field is keyed from the source."""
    k = (it.set, it.doc, it.field, "rev")
    if band == "proceed":
        return it.right
    if band == "review" and shown:
        if it.right:
            return u(*k) > 0.002
        return u(*k) >= MISS[tier(it.q)]
    return u(*k) > SCRATCH[tier(it.q)]
