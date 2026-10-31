"""fieldkit.routing (book layer v3.4, Chapter 27): the confidence router.

A confidence score is a claim about frequency: of the fields that get this score, this share is right. It is only
worth routing on after it has been checked against the customer's experts. This module holds the pieces Chapter 27
uses at Caldwell Mutual:

- reliability bins, expected calibration error and score resolution (how many distinct values a score takes);
- a correctness model fitted on the expert-scored history (logistic regression over several signals, then
  isotonic calibration), because a model asked how sure it is reports inflated numbers;
- threshold selection with a Wilson lower bound on a held-out half, and a floor below which no recommendation
  is shown;
- deterministic evidence gates that fail closed (no evidence, exhausted budget, conflicting sources, not in the
  documents) and are never multiplied into a probability;
- the router itself, the post-review error rate and a drift monitor that says when to re-calibrate;
- the threshold decision record a risk team signs.

Standard library only. Package version stays 0.1.0.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Iterable, Sequence

PROCEED, REVIEW, ESCALATE = "proceed", "review", "escalate"
BANDS = (PROCEED, REVIEW, ESCALATE)
FAIL_CLOSED = ("no evidence", "budget exhausted", "conflicting sources", "not in the documents")


# ---------------------------------------------------------------- measurement
def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for k successes in n trials."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


@dataclass(frozen=True)
class Bin:
    lo: float
    hi: float
    n: int
    mean_score: float
    accuracy: float


def reliability(scores: Sequence[float], outcomes: Sequence[bool], bins: int = 10) -> list[Bin]:
    """Equal-width reliability bins: mean score against observed accuracy in each bin."""
    out = []
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        idx = [i for i, s in enumerate(scores) if (lo <= s < hi) or (b == bins - 1 and s == 1.0)]
        if idx:
            out.append(Bin(lo, hi, len(idx), sum(scores[i] for i in idx) / len(idx),
                           sum(bool(outcomes[i]) for i in idx) / len(idx)))
    return out


def ece(scores: Sequence[float], outcomes: Sequence[bool], bins: int = 10) -> float:
    """Expected calibration error: bin-weighted gap between mean score and accuracy."""
    n = len(scores)
    return sum(b.n / n * abs(b.mean_score - b.accuracy) for b in reliability(scores, outcomes, bins))


def resolution(scores: Iterable[float], places: int = 3) -> int:
    """How many distinct values the score takes. A threshold can only sit between two of them."""
    return len({round(s, places) for s in scores})


def auroc(scores: Sequence[float], outcomes: Sequence[bool]) -> float:
    """Probability that a right item outscores a wrong one (ties count half)."""
    pos = sorted(s for s, o in zip(scores, outcomes) if o)
    neg = sorted(s for s, o in zip(scores, outcomes) if not o)
    if not pos or not neg:
        return float("nan")
    wins = 0.0
    import bisect
    for s in pos:
        lo = bisect.bisect_left(neg, s)
        hi = bisect.bisect_right(neg, s)
        wins += lo + 0.5 * (hi - lo)
    return wins / (len(pos) * len(neg))


# ---------------------------------------------------------------- calibration
class Isotonic:
    """Pool-adjacent-violators isotonic calibration of one score against expert outcomes."""

    def __init__(self):
        self.xs: list[float] = []
        self.ys: list[float] = []

    def fit(self, scores: Sequence[float], outcomes: Sequence[bool]) -> "Isotonic":
        pairs = sorted(zip(scores, outcomes))
        blocks = []  # [sum_y, count, min_x, max_x]
        for x, y in pairs:
            blocks.append([float(y), 1, x, x])
            while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
                s, c, lo, hi = blocks.pop()
                blocks[-1][0] += s; blocks[-1][1] += c; blocks[-1][3] = hi
        self.xs = [(b[2] + b[3]) / 2 for b in blocks]
        self.ys = [b[0] / b[1] for b in blocks]
        return self

    def predict(self, s: float) -> float:
        xs, ys = self.xs, self.ys
        if not xs:
            raise ValueError("fit first")
        if s <= xs[0]:
            return ys[0]
        if s >= xs[-1]:
            return ys[-1]
        import bisect
        j = bisect.bisect_right(xs, s)
        x0, x1, y0, y1 = xs[j - 1], xs[j], ys[j - 1], ys[j]
        return y0 + (y1 - y0) * (s - x0) / (x1 - x0) if x1 > x0 else y1


def _solve(A: list[list[float]], b: list[float]) -> list[float]:
    """Gaussian elimination with partial pivoting (small dense systems)."""
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        if abs(M[c][c]) < 1e-12:
            continue
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f:
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    x = [0.0] * n
    for c in range(n - 1, -1, -1):
        x[c] = (M[c][n] - sum(M[c][k] * x[k] for k in range(c + 1, n))) / M[c][c] if abs(M[c][c]) > 1e-12 else 0.0
    return x


def _sig(z: float) -> float:
    return 1 / (1 + math.exp(-max(-30.0, min(30.0, z))))


@dataclass
class CorrectnessModel:
    """Predicts whether a field value is right from several signals, fitted on expert-scored history.

    features(item) -> list[float]. Ridge logistic regression by Newton steps (deterministic), then isotonic
    calibration on the same history so the output reads as a frequency."""
    features: Callable[[object], list[float]]
    names: tuple[str, ...] = ()
    l2: float = 1.0
    iters: int = 25
    w: list[float] = field(default_factory=list)
    iso: Isotonic | None = None
    fitted_on: str = ""

    def raw(self, item) -> float:
        x = self.features(item)
        return _sig(self.w[0] + sum(a * b for a, b in zip(self.w[1:], x)))

    def fit(self, items: Sequence, outcomes: Sequence[bool], label: str = "") -> "CorrectnessModel":
        X = [[1.0] + list(self.features(it)) for it in items]
        y = [1.0 if o else 0.0 for o in outcomes]
        d = len(X[0])
        w = [0.0] * d
        for _ in range(self.iters):  # Newton steps (iteratively reweighted least squares) with a small ridge
            g = [0.0] * d
            H = [[0.0] * d for _ in range(d)]
            for xi, yi in zip(X, y):
                p = _sig(sum(a * b for a, b in zip(w, xi)))
                r = p * (1 - p)
                for j in range(d):
                    g[j] += (p - yi) * xi[j]
                    rj = r * xi[j]
                    if rj:
                        Hj = H[j]
                        for k in range(d):
                            Hj[k] += rj * xi[k]
            for j in range(1, d):
                g[j] += self.l2 * w[j]
                H[j][j] += self.l2
            step = _solve(H, g)
            w = [a - b for a, b in zip(w, step)]
            if max(abs(v) for v in step) < 1e-6:
                break
        self.w = w
        self.iso = Isotonic().fit([self.raw(it) for it in items], outcomes)
        self.fitted_on = label
        return self

    def score(self, item) -> float:
        return self.iso.predict(self.raw(item)) if self.iso else self.raw(item)


# ---------------------------------------------------------------- thresholds
@dataclass(frozen=True)
class Thresholds:
    proceed: float          # score at or above: value written without review
    floor: float            # score below: escalate, and no recommendation is shown
    target: float           # accuracy promised on proceed-band fields
    lower_bound: float      # Wilson lower bound of proceed-band accuracy on the checked half
    checked_n: int          # proceed-band fields on the checked half


def choose_proceed(scores: Sequence[float], outcomes: Sequence[bool], target: float = 0.98,
                   min_n: int = 200, grid: Iterable[float] | None = None) -> tuple[float, float, int] | None:
    """Lowest threshold whose proceed band has a Wilson lower bound at or above target (on the data given)."""
    grid = list(grid) if grid is not None else [x / 1000 for x in range(500, 1000, 5)]
    for t in grid:
        idx = [i for i, s in enumerate(scores) if s >= t]
        if len(idx) < min_n:
            continue
        k = sum(bool(outcomes[i]) for i in idx)
        lo, _ = wilson(k, len(idx))
        if lo >= target:
            return t, lo, len(idx)
    return None


def choose_floor(scores: Sequence[float], outcomes: Sequence[bool], max_acc: float = 0.5, width: float = 0.2,
                 grid: Iterable[float] | None = None) -> float:
    """Lowest threshold t such that every window [x, x + width) at or above t holds suggestions that are right
    more than max_acc of the time. Below t a suggestion is as likely to mislead a reviewer as to help, so none is
    shown."""
    grid = sorted(grid) if grid is not None else [x / 100 for x in range(5, 96)]
    ok = []
    for t in grid:
        idx = [i for i, s in enumerate(scores) if t <= s < t + width]
        ok.append(len(idx) < 20 or sum(bool(outcomes[i]) for i in idx) / len(idx) > max_acc)
    for j, t in enumerate(grid):
        if all(ok[j:]):
            return t
    return grid[-1]


def set_thresholds(fit_scores, fit_outcomes, check_scores, check_outcomes, target=0.98, floor_acc=0.5,
                   min_n=200, marginal_min=0.95) -> Thresholds:
    """Choose on one half, report the bound on the other. Two conditions for the proceed threshold: the band's
    Wilson lower bound meets the target, and no field enters the band with a calibrated score below marginal_min
    (the band average must not hide a slice of coin flips). Raises if the target cannot be met."""
    c = choose_proceed(fit_scores, fit_outcomes, target, min_n,
                       grid=[x / 1000 for x in range(int(marginal_min * 1000), 1000, 5)])
    if c is None:
        raise ValueError(f"no proceed threshold reaches {target:.0%} on the fitting half")
    t = c[0]
    while True:
        idx = [i for i, s in enumerate(check_scores) if s >= t]
        k = sum(bool(check_outcomes[i]) for i in idx)
        lo, _ = wilson(k, len(idx))
        if lo >= target or t >= 0.995:
            break
        t = round(t + 0.005, 3)
    if lo < target:
        raise ValueError("target not met on the checked half")
    return Thresholds(t, choose_floor(fit_scores, fit_outcomes, floor_acc), target, lo, len(idx))


# ---------------------------------------------------------------- evidence gates and the router
@dataclass(frozen=True)
class Evidence:
    """Deterministic facts about one field value. None means the check does not apply to this field."""
    found_in_source: bool               # the value appears in the document text the extractor read
    system_check: bool | None = None    # e.g. policy number exists in claims-core; loss date passes V-127
    sources_agree: bool | None = None   # e.g. email body and attached form give the same loss date
    budget_ok: bool = True              # retries, tokens and time stayed inside the run's budget


def gate(ev: Evidence) -> str | None:
    """Return a fail-closed reason, or None. Order matters only for the reason recorded."""
    if not ev.budget_ok:
        return "budget exhausted"
    if ev.sources_agree is False:
        return "conflicting sources"
    if not ev.found_in_source and ev.system_check is not True:
        return "no evidence"
    return None


@dataclass(frozen=True)
class Route:
    band: str
    reason: str
    score: float
    show_recommendation: bool


def route_field(score: float, ev: Evidence, th: Thresholds) -> Route:
    """Evidence first, then the calibrated score. Evidence is never turned into probability."""
    why = gate(ev)
    if why:
        return Route(ESCALATE, why, score, False)
    if score < th.floor:
        return Route(ESCALATE, "below floor", score, False)
    if ev.system_check is False:
        return Route(REVIEW, "system check failed", score, True)
    if score >= th.proceed:
        return Route(PROCEED, "calibrated score", score, True)
    return Route(REVIEW, "calibrated score", score, True)


def route_document(routes: Sequence[Route], fields: Sequence[str] = (), critical: Iterable[str] = (),
                   max_blank: int = 3, critical_escalates: bool = False) -> tuple[str, str]:
    """Combine field routes into the document's band and the reason.

    Escalate (a specialist works the document from the source, no suggestions) when any field failed closed, or
    when more than max_blank fields (or any critical field, if critical_escalates) are below the floor. Review when
    any field is in the review band or below the floor (below-floor fields are shown blank, keyed from the source).
    Proceed otherwise."""
    crit = set(critical)
    fc = [r.reason for r in routes if r.reason in FAIL_CLOSED]
    if fc:
        return ESCALATE, fc[0]
    below = [f for r, f in zip(routes, fields or [""] * len(routes)) if r.reason == "below floor"]
    if critical_escalates and any(f in crit for f in below):
        return ESCALATE, "critical field below floor"
    if len(below) > max_blank:
        return ESCALATE, "too many fields below floor"
    if below or any(r.band == REVIEW for r in routes):
        return REVIEW, "flagged fields"
    return PROCEED, "all fields in proceed band, evidence passed"


@dataclass(frozen=True)
class AnswerCheck:
    """The evidence gate for drafted answers (Chapter 23's question set): an answer may be shown only if every
    quoted span is present verbatim in a retrieved, permitted, in-force passage and the question's key terms are
    covered by the passages it quotes. Below min_coverage the answer is 'not in the documents' and goes to a person;
    between min_coverage and review_below it goes to review; only full coverage may proceed."""
    min_coverage: float = 0.6
    review_below: float = 0.8

    @staticmethod
    def coverage(quotes: Sequence[str], passages: Sequence[str], key_terms: Sequence[str]) -> float:
        cited = "\n".join(p for p in passages if any(q.lower() in p.lower() for q in quotes)).lower()
        return sum(t.lower() in cited for t in key_terms) / max(1, len(key_terms))

    def check(self, quotes: Sequence[str], passages: Sequence[str], key_terms: Sequence[str]) -> str | None:
        if not quotes:
            return "not in the documents"
        text = "\n".join(passages).lower()
        if any(q.lower() not in text for q in quotes):
            return "not in the documents"
        return None if self.coverage(quotes, passages, key_terms) >= self.min_coverage else "not in the documents"

    def route(self, quotes: Sequence[str], passages: Sequence[str], key_terms: Sequence[str]) -> tuple[str, str]:
        why = self.check(quotes, passages, key_terms)
        if why:
            return ESCALATE, why
        if self.coverage(quotes, passages, key_terms) < self.review_below:
            return REVIEW, "key terms partly covered"
        return PROCEED, "quotes verbatim, key terms covered"


def post_review_error(final_values_right: Sequence[bool]) -> tuple[float, float, float]:
    """Share of fields still wrong after the whole system (model, router and people), with a Wilson interval."""
    n = len(final_values_right)
    k = sum(not r for r in final_values_right)
    lo, hi = wilson(k, n)
    return k / max(1, n), lo, hi


@dataclass
class DriftMonitor:
    """Weekly audit of proceed-band fields scored by the customer's experts. Re-calibrate when the Wilson lower
    bound of the error rate crosses the promise, or when the score distribution moves (PSI) past a line."""
    promise_error: float = 0.02
    psi_line: float = 0.2

    @staticmethod
    def psi(base: Sequence[float], now: Sequence[float], bins: int = 10) -> float:
        def hist(xs):
            h = [0] * bins
            for x in xs:
                h[min(bins - 1, int(x * bins))] += 1
            return [(c + 0.5) / (len(xs) + 0.5 * bins) for c in h]
        a, b = hist(base), hist(now)
        return sum((q - p) * math.log(q / p) for p, q in zip(a, b))

    def check(self, wrong: int, n: int, base_scores=None, now_scores=None) -> tuple[bool, str]:
        lo, _ = wilson(wrong, n)
        if lo > self.promise_error:
            return True, f"error lower bound {lo:.1%} above {self.promise_error:.0%}"
        if base_scores is not None and now_scores is not None:
            p = self.psi(base_scores, now_scores)
            if p > self.psi_line:
                return True, f"score shift PSI {p:.2f} above {self.psi_line}"
        return False, "within promise"


@dataclass(frozen=True)
class ThresholdRecord:
    """The decision record a risk team signs. A threshold without one of these is a guess."""
    proceed: float
    floor: float
    target: str
    calibration_set: str
    checked_on: str
    lower_bound: float
    routing: str
    post_review_error: str
    owner: str
    signed_by: tuple[str, ...]
    day: int
    review_trigger: str

    def missing(self) -> list[str]:
        miss = [k for k in ("target", "calibration_set", "checked_on", "routing", "post_review_error", "owner",
                            "review_trigger") if not getattr(self, k)]
        if not self.signed_by:
            miss.append("signed_by")
        return miss
