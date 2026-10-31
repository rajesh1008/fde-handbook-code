"""fieldkit v3.7 (Chapter 30): small models, fine-tuning and the cost curve on site.

The fine-tune evaluation suite: a paired comparison of two arms on the same expert-scored documents (Wilson
intervals and an exact McNemar test on the discordant pairs), per-class accuracy, a familiarity check and an
absent-class guard for document classes the training set never contained, cost per document and monthly cost by
volume with the crossover between serving options, the signed training-data record, the model-risk classification
change and the switch gate that keeps the prompted arm in production until every condition holds.
"""
from __future__ import annotations

from dataclasses import dataclass, field, fields
from math import comb, sqrt
from typing import Callable, Iterable, Sequence


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    m = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - m), min(1.0, c + m))


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact test on the discordant pairs (b: only arm A right, c: only arm B right)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


@dataclass
class PairedComparison:
    n: int
    both_right: int
    a_only: int
    b_only: int
    both_wrong: int

    @property
    def right_a(self) -> int:
        return self.both_right + self.a_only

    @property
    def right_b(self) -> int:
        return self.both_right + self.b_only

    @property
    def p_value(self) -> float:
        return mcnemar_exact(self.a_only, self.b_only)

    def ci(self, arm: str) -> tuple[float, float]:
        return wilson(self.right_a if arm == "a" else self.right_b, self.n)

    def verdict(self, alpha: float = 0.05) -> str:
        if self.p_value >= alpha:
            return "no detectable difference"
        return "A better" if self.a_only > self.b_only else "B better"


def paired_compare(pred_a: Sequence, pred_b: Sequence, truth: Sequence,
                   right: Callable[[object, object], bool] | None = None) -> PairedComparison:
    if not (len(pred_a) == len(pred_b) == len(truth)):
        raise ValueError("both arms must be scored on the same documents")
    ok = right or (lambda p, t: p == t)
    cells = [0, 0, 0, 0]
    for a, b, t in zip(pred_a, pred_b, truth):
        ra, rb = ok(a, t), ok(b, t)
        cells[0 if ra and rb else 1 if ra else 2 if rb else 3] += 1
    return PairedComparison(len(truth), *cells)


def per_class(pred: Sequence, truth: Sequence, key: Sequence | None = None,
              right: Callable[[object, object], bool] | None = None) -> dict:
    """Right and total per class (or per key, such as the document kind). Returns {class: (right, n)}."""
    ok = right or (lambda p, t: p == t)
    out: dict = {}
    for i, (p, t) in enumerate(zip(pred, truth)):
        k = key[i] if key is not None else t
        r, n = out.get(k, (0, 0))
        out[k] = (r + int(ok(p, t)), n + 1)
    return out


def familiarity(tokens: Iterable[str], vocab: set) -> float:
    toks = list(tokens)
    return sum(t in vocab for t in toks) / len(toks) if toks else 0.0


@dataclass
class GuardRule:
    name: str
    test: Callable[[list], bool]
    route: str
    owner: str


@dataclass
class Hold:
    reason: str
    route: str
    familiarity: float


class AbsentClassGuard:
    """Holds documents that look unlike anything in training, and documents a deterministic owner rule claims.

    A model fine-tuned on a set that never contained a class will still answer with a class it knows. The guard
    runs before the model's answer is used: owner rules first (they are cheap and exact), then familiarity.
    """

    def __init__(self, vocab: set, threshold: float, rules: Sequence[GuardRule] = ()):
        if not 0 < threshold < 1:
            raise ValueError("threshold must be between 0 and 1")
        self.vocab, self.threshold, self.rules = set(vocab), threshold, list(rules)

    def check(self, tokens: Sequence[str]) -> Hold | None:
        f = familiarity(tokens, self.vocab)
        for r in self.rules:
            if r.test(list(tokens)):
                return Hold(r.name, r.route, f)
        if f < self.threshold:
            return Hold("unfamiliar", "review queue", f)
        return None


def cost_per_doc(in_tokens: float, out_tokens: float, in_price_per_m: float, out_price_per_m: float) -> float:
    return (in_tokens * in_price_per_m + out_tokens * out_price_per_m) / 1e6


@dataclass
class ServingOption:
    name: str
    per_doc: float
    fixed_monthly: float = 0.0
    ownership_monthly: float = 0.0

    def monthly(self, volume: float) -> float:
        return self.fixed_monthly + self.ownership_monthly + self.per_doc * volume


def monthly_cost(opt: ServingOption, volume: float) -> float:
    return opt.monthly(volume)


def crossover(a: ServingOption, b: ServingOption) -> float | None:
    """Monthly volume at which a and b cost the same, or None if one is cheaper at every volume."""
    dv = a.per_doc - b.per_doc
    df = (b.fixed_monthly + b.ownership_monthly) - (a.fixed_monthly + a.ownership_monthly)
    if dv == 0:
        return None
    v = df / dv
    return v if v > 0 else None


def learning_crossover(sizes: Sequence[int], accs: Sequence[float], target: float) -> int | None:
    for s, a in zip(sizes, accs):
        if a >= target:
            return s
    return None


@dataclass
class TrainingDataRecord:
    """The signed record that has to exist before customer data trains anything."""
    dataset: str = ""
    source_system: str = ""
    data_owner: str = ""
    label_owner: str = ""
    purpose: str = ""
    permitted_uses: str = ""
    location: str = ""
    retention: str = ""
    derived_artifacts: str = ""
    excluded: str = ""
    dedupe_against: str = ""
    signed_by: list = field(default_factory=list)
    signed_day: int | None = None

    def missing(self) -> list[str]:
        out = [f.name for f in fields(self) if f.name not in ("signed_by", "signed_day") and not getattr(self, f.name)]
        if self.data_owner and self.data_owner not in self.signed_by:
            out.append("signature of data_owner")
        if self.label_owner and self.label_owner not in self.signed_by:
            out.append("signature of label_owner")
        if self.signed_day is None:
            out.append("signed_day")
        return out

    def ok(self) -> bool:
        return not self.missing()


def risk_class(trained_on_customer_data: bool, affects_decisions: bool, vendor_model: bool = True) -> str:
    if not affects_decisions:
        return "outside model-risk scope"
    if trained_on_customer_data:
        return "model developed with customer data: full scope (validation before use, retrain is a model change)"
    if vendor_model:
        return "third-party model use: vendor due diligence and use-case review"
    return "in-house model: full scope"


class SwitchGate:
    """Conditions that must all hold before the fine-tuned arm replaces the prompted arm in production."""

    def __init__(self, conditions: Sequence[str]):
        self.conditions = list(conditions)

    def check(self, evidence: dict) -> tuple[bool, list[str]]:
        missing = [c for c in self.conditions if not evidence.get(c)]
        return (not missing, missing)
