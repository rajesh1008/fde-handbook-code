"""Evaluation suites built with the customer's experts (Chapter 26, fieldkit book layer v3.3; package stays 0.1.0).

The pieces a forward deployed engineer needs when the customer's experts, not the vendor, define correct:

* `gold_value_ready` and `GoldValuePolicy`: a gold value taken from a customer record is only used once the record
  is old enough to have been corrected (Chapter 7: at least 14 days).
* `percent_agreement`, `cohen_kappa`, `calibration_report`: agreement between two expert annotators, per field,
  against a line that depends on whether the field is exact or a judgment.
* `Adjudicator`: disagreements go to one named owner, who decides each with a reason code; the gold set refuses to
  build while any disagreement is undecided.
* `JudgeValidation`, `corrected_rate`, `corrected_interval`, `flip_rate`: an automated judge is a classifier of the
  expert's verdict. It is validated by true-positive and true-negative rates on expert-labeled items it was not
  tuned on, its raw pass rate is corrected for its known bias, and repeat runs are checked for self-inconsistency.
  Kappa is for two peers; it is not how a judge is validated.
* `four_cells` and `CustomerGate`: a regression gate per customer, with that customer's owner, scorer, document
  set and critical fields, that reports correct-on-both, gained, lost and wrong-on-both and blocks on lost
  critical items as well as on the aggregate.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

# ---------------------------------------------------------------- gold values ------------------------------------

def gold_value_ready(record_age_days, min_age_days=14):
    """A customer record is usable as a gold value only once it has had time to be corrected."""
    return record_age_days >= min_age_days


@dataclass
class GoldValuePolicy:
    min_age_days: int = 14

    def split(self, items, age_of):
        """items: iterable; age_of(item) -> days. Returns (ready, held)."""
        ready, held = [], []
        for it in items:
            (ready if gold_value_ready(age_of(it), self.min_age_days) else held).append(it)
        return ready, held

# ---------------------------------------------------------------- agreement ---------------------------------------

def percent_agreement(a, b):
    if len(a) != len(b) or not a:
        raise ValueError("two annotators must label the same, non-empty list of items")
    return sum(x == y for x, y in zip(a, b)) / len(a)


def cohen_kappa(a, b):
    """Cohen's kappa for two annotators who labeled the same items (any hashable labels)."""
    po = percent_agreement(a, b)
    n = len(a)
    cats = set(a) | set(b)
    pe = sum((list(a).count(c) / n) * (list(b).count(c) / n) for c in cats)
    if pe == 1.0:
        return 1.0 if po == 1.0 else 0.0
    return (po - pe) / (1 - pe)


def calibration_report(scores_a, scores_b, exact_fields, exact_line=0.8, judgment_line=0.6):
    """scores_x: {field: [label per item]}. Returns {field: (kappa, line, ok)}; exact fields need the higher line."""
    out = {}
    for f in scores_a:
        k = cohen_kappa(scores_a[f], scores_b[f])
        line = exact_line if f in exact_fields else judgment_line
        out[f] = (round(k, 2), line, k >= line)
    return out

# ---------------------------------------------------------------- adjudication ------------------------------------

@dataclass
class Disagreement:
    item: str
    field: str
    a: object
    b: object
    decided: object = None
    reason: str = ""
    by: str = ""


class Adjudicator:
    REASONS = ("rubric gap", "reading error", "document ambiguous")

    def __init__(self, owner):
        parts = (owner or "").split()
        if len(parts) < 2 or not all(w[0].isupper() for w in parts) or parts[-1].lower() in ("team", "group", "desk"):
            raise ValueError("the adjudicator is a named person, not a team")
        self.owner = owner
        self.open: list[Disagreement] = []
        self.closed: list[Disagreement] = []

    def compare(self, labels_a, labels_b):
        """labels_x: {(item, field): value}. Records every disagreement on the shared items."""
        for k in sorted(set(labels_a) & set(labels_b)):
            if labels_a[k] != labels_b[k]:
                self.open.append(Disagreement(k[0], k[1], labels_a[k], labels_b[k]))
        return list(self.open)

    def decide(self, d, value, reason):
        if reason not in self.REASONS:
            raise ValueError(f"reason must be one of {self.REASONS}")
        d.decided, d.reason, d.by = value, reason, self.owner
        self.open.remove(d)
        self.closed.append(d)

    def gold(self, *label_sets):
        """Merge label sets; refuse while anything is undecided."""
        if self.open:
            raise RuntimeError(f"{len(self.open)} disagreements undecided; the gold set cannot be built")
        merged = {}
        for ls in label_sets:
            merged.update(ls)
        for d in self.closed:
            merged[(d.item, d.field)] = d.decided
        return merged

    def reason_counts(self):
        out = {r: 0 for r in self.REASONS}
        for d in self.closed:
            out[d.reason] += 1
        return out

# ---------------------------------------------------------------- judges ------------------------------------------

def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


@dataclass
class JudgeValidation:
    """Judge verdicts against the expert's verdicts on the same items (True = pass)."""
    judge: list
    expert: list

    def __post_init__(self):
        if len(self.judge) != len(self.expert):
            raise ValueError("judge and expert must score the same items")

    @property
    def tp(self): return sum(j and e for j, e in zip(self.judge, self.expert))
    @property
    def fn(self): return sum((not j) and e for j, e in zip(self.judge, self.expert))
    @property
    def fp(self): return sum(j and (not e) for j, e in zip(self.judge, self.expert))
    @property
    def tn(self): return sum((not j) and (not e) for j, e in zip(self.judge, self.expert))
    @property
    def tpr(self): return self.tp / max(1, self.tp + self.fn)
    @property
    def tnr(self): return self.tn / max(1, self.tn + self.fp)

    def verdict(self, min_tpr=0.90, min_tnr=0.80, min_fail=30):
        reasons = []
        if self.tn + self.fp < min_fail:
            reasons.append(f"only {self.tn + self.fp} expert fails; need {min_fail} to measure TNR")
        if self.tpr < min_tpr:
            reasons.append(f"TPR {self.tpr:.2f} < {min_tpr}")
        if self.tnr < min_tnr:
            reasons.append(f"TNR {self.tnr:.2f} < {min_tnr}: the judge passes what the expert fails")
        return (not reasons, reasons)

    def verdict_with_repeats(self, runs, max_flip=0.05, **kw):
        ok, reasons = self.verdict(**kw)
        fr = flip_rate(runs)
        if fr > max_flip:
            reasons.append(f"{fr:.1%} of verdicts change across repeat runs (limit {max_flip:.0%})")
        return (not reasons, reasons)


def corrected_rate(q, tpr, tnr):
    """Correct a judge's raw pass rate q for its known TPR and TNR (clamped to 0..1)."""
    d = tpr + tnr - 1
    if d <= 0:
        raise ValueError("judge no better than chance; its pass rate cannot be corrected")
    return min(1.0, max(0.0, (q + tnr - 1) / d))


def corrected_interval(judge_target, judge_cal, expert_cal, reps=2000, seed=26, level=0.95):
    """Bootstrap interval for the corrected pass rate: resample the calibration items and the target items."""
    rng = random.Random(seed)
    v = JudgeValidation(judge_cal, expert_cal)
    point = corrected_rate(sum(judge_target) / len(judge_target), v.tpr, v.tnr)
    cal = list(zip(judge_cal, expert_cal))
    est = []
    for _ in range(reps):
        c = [cal[rng.randrange(len(cal))] for _ in cal]
        t = [judge_target[rng.randrange(len(judge_target))] for _ in judge_target]
        vv = JudgeValidation([x for x, _ in c], [y for _, y in c])
        try:
            est.append(corrected_rate(sum(t) / len(t), vv.tpr, vv.tnr))
        except ValueError:
            continue
    est.sort()
    lo = est[int((1 - level) / 2 * len(est))]
    hi = est[int((1 + level) / 2 * len(est)) - 1]
    return point, lo, hi


def flip_rate(runs):
    """runs: list of verdict lists from repeated judge runs on the same items. Share of items not unanimous."""
    n = len(runs[0])
    return sum(len({r[i] for r in runs}) > 1 for i in range(n)) / n

# ---------------------------------------------------------------- regression gate ---------------------------------

def four_cells(before, after):
    """before/after: {key: bool correct}. Returns lists of keys per cell."""
    cells = {"correct on both": [], "gained": [], "lost": [], "wrong on both": []}
    for k in before:
        b, a = before[k], after[k]
        cells["correct on both" if b and a else "gained" if a else "lost" if b else "wrong on both"].append(k)
    return cells


def weighted(results, weight_of):
    num = sum(weight_of(k) for k, ok in results.items() if ok)
    den = sum(weight_of(k) for k in results)
    return num / den


@dataclass
class CustomerGate:
    customer: str
    owner: str
    scorer: str
    document_set: str
    critical_fields: tuple
    max_drop_points: float = 0.5
    max_lost_critical: int = 0
    lines: list = field(default_factory=list)

    def check(self, before, after, weight_of=lambda k: 1.0, field_of=lambda k: k[1], signed_off=()):
        """before/after: {(item, field): bool} scored by this customer's scorer on this customer's set.
        Returns (status, reasons, cells, before_acc, after_acc); status is "pass", "owner review" or "block".
        An aggregate drop blocks. Lost critical items go to the owner; the keys the owner has reviewed and
        accepted are passed back as signed_off."""
        if set(before) != set(after):
            raise ValueError("before and after must be scored on the same items")
        wb, wa = weighted(before, weight_of), weighted(after, weight_of)
        cells = four_cells(before, after)
        lost_crit = [k for k in cells["lost"] if field_of(k) in self.critical_fields and k not in set(signed_off)]
        reasons, status = [], "pass"
        if (wb - wa) * 100 > self.max_drop_points:
            reasons.append(f"weighted accuracy fell {100 * (wb - wa):.1f} points")
            status = "block"
        if len(lost_crit) > self.max_lost_critical:
            status = "block" if status == "block" else "owner review"
            by = {}
            for k in lost_crit:
                by[field_of(k)] = by.get(field_of(k), 0) + 1
            reasons.append(f"{len(lost_crit)} lost items on critical fields {dict(sorted(by.items()))}; "
                           f"needs {self.owner}")
        self.lines = [f"{self.customer} gate ({self.document_set}, scored by {self.scorer})",
                      f"  weighted accuracy {wb:.1%} -> {wa:.1%}",
                      "  " + ", ".join(f"{c} {len(v)}" for c, v in cells.items())]
        return (status, reasons, cells, wb, wa)
