"""fieldkit v3.1 (Chapter 24): surface where they work, brain where it is governed.

Four pieces, all pure Python and deterministic under a seed:
- the option-scoring model: weighted dimensions, totals on a 0-100 scale, the lead of one option over the best
  other, flip points per weight and win shares under random weight draws (the sensitivity analysis);
- the fan-out model: sources with a median latency and a lognormal spread, called in sequence or in parallel,
  with an optional per-source timeout that turns a slow source into a marked partial answer;
- the token broker: one user assertion crosses the boundary, the broker exchanges it on behalf of the user for a
  token per downstream audience, refuses assertions minted for another audience, and caches by user and audience;
- the mode flag: live, shadow or off, enforced in the brain on every turn, never only in the surface.
The turn contract (TurnRequest, TurnResponse) is the one call per turn that crosses the boundary."""
from __future__ import annotations
import math, random
from collections import Counter
from dataclasses import dataclass, field

MODES = ("live", "shadow", "off")


# ---------------------------------------------------------------- option scoring
@dataclass(frozen=True)
class Option:
    key: str
    name: str
    scores: dict  # dimension -> 1..5, each with a written reason kept beside the model

    def __post_init__(self):
        bad = {d: s for d, s in self.scores.items() if not (1 <= s <= 5)}
        if bad:
            raise ValueError(f"scores must be 1..5: {bad}")


def total(option: Option, weights: dict) -> float:
    w = sum(weights.values())
    missing = set(weights) - set(option.scores)
    if missing:
        raise KeyError(f"{option.key} has no score for {sorted(missing)}")
    return 100.0 * sum(weights[d] * option.scores[d] for d in weights) / (5.0 * w)


def contributions(option: Option, weights: dict) -> dict:
    w = sum(weights.values())
    return {d: 100.0 * weights[d] * option.scores[d] / (5.0 * w) for d in weights}


def rank(options, weights):
    return sorted(((o.key, total(o, weights)) for o in options), key=lambda kv: -kv[1])


def lead(options, weights, key):
    mine = next(total(o, weights) for o in options if o.key == key)
    other = max((total(o, weights), o.key) for o in options if o.key != key)
    return mine - other[0], other[1]


def scaled(weights, dim, factor):
    w = dict(weights); w[dim] = weights[dim] * factor
    return w


def flip_point(options, weights, dim, key, lo=0.0, hi=4.0, step=0.01):
    """Multipliers on one weight (others unchanged) at which `key` stops winning, searching down then up."""
    def wins(f):
        return rank(options, scaled(weights, dim, f))[0][0] == key
    down = up = None
    f = 1.0
    while f - step >= lo - 1e-9:
        f = round(f - step, 4)
        if not wins(f):
            down = f; break
    f = 1.0
    while f + step <= hi + 1e-9:
        f = round(f + step, 4)
        if not wins(f):
            up = f; break
    return down, up


def sensitivity(options, weights, key, factors=(0.5, 1.5)):
    out = {}
    for d in weights:
        out[d] = tuple(lead(options, scaled(weights, d, f), key) for f in factors)
    return out


def weight_draws(options, weights, n=2000, concentration=60.0, seed=24):
    """Dirichlet draws centred on the agreed weights; returns win counts per option."""
    rng = random.Random(seed); tot = sum(weights.values()); wins = Counter()
    for _ in range(n):
        g = {d: rng.gammavariate(concentration * w / tot, 1.0) for d, w in weights.items()}
        wins[rank(options, g)[0][0]] += 1
    return wins


# ---------------------------------------------------------------- fan-out
@dataclass(frozen=True)
class Source:
    name: str
    median_ms: float
    sigma: float = 0.35
    audience: str = ""

    def sample(self, rng: random.Random) -> float:
        return self.median_ms * math.exp(self.sigma * rng.gauss(0.0, 1.0))


@dataclass
class Turn:
    total_ms: float
    fanout_ms: float
    calls: dict            # source -> (start_ms, end_ms) relative to the start of the fan-out
    partial: list          # sources cut by the timeout
    slowest: str


def run_turn(sources, rng, mode="parallel", exchange_ms=None, model_ms=1000.0, verify_ms=120.0,
             timeout_ms=None, crossing_ms=60.0):
    """One turn: crossing, then the fan-out (token exchange + source call per source), model, verification."""
    exchange_ms = exchange_ms or {}
    lat = {s.name: s.sample(rng) for s in sources}
    calls, partial, t = {}, [], 0.0
    for s in sources:
        x = exchange_ms.get(s.name, 0.0)
        dur = lat[s.name]
        if timeout_ms is not None and dur > timeout_ms:
            dur = timeout_ms; partial.append(s.name)
        start = t if mode == "sequential" else 0.0
        calls[s.name] = (start, start + x + dur)
        if mode == "sequential":
            t = start + x + dur
    fan = max(e for _, e in calls.values())
    slowest = max(calls, key=lambda k: calls[k][1] - calls[k][0])
    return Turn(crossing_ms + fan + model_ms + verify_ms, fan, calls, partial, slowest)


def percentile(xs, p):
    xs = sorted(xs)
    k = (len(xs) - 1) * p / 100.0
    f, c = math.floor(k), math.ceil(k)
    return xs[f] if f == c else xs[f] + (xs[c] - xs[f]) * (k - f)


# ---------------------------------------------------------------- token brokerage
class AudienceMismatch(Exception):
    pass


@dataclass(frozen=True)
class Token:
    subject: str
    audience: str
    issued: float
    expires: float
    actor: str = ""          # who acts on the subject's behalf (the brain), empty for the user's own assertion
    scopes: tuple = ()


class TokenBroker:
    """Exchanges the user's assertion (audience = the brain) for per-source tokens on behalf of the user."""

    def __init__(self, brain_audience="api://nl-brain", actor="nl-brain", ttl_s=900, exchange_ms=95.0,
                 cache_ms=4.0, scopes=None):
        self.brain_audience, self.actor, self.ttl = brain_audience, actor, ttl_s
        self.exchange_ms, self.cache_ms = exchange_ms, cache_ms
        self.scopes = scopes or {}
        self.cache, self.stats = {}, Counter()

    def accept(self, assertion: Token, now: float) -> None:
        if assertion.audience != self.brain_audience:
            self.stats["refused_audience"] += 1
            raise AudienceMismatch(f"assertion audience {assertion.audience!r} is not {self.brain_audience!r}")
        if now >= assertion.expires:
            self.stats["refused_expired"] += 1
            raise AudienceMismatch("assertion expired")

    def exchange(self, assertion: Token, audience: str, now: float):
        self.accept(assertion, now)
        key = (assertion.subject, audience)
        tok = self.cache.get(key)
        if tok and tok.expires - now > 60:      # never hand out a token with under a minute left
            self.stats["cache_hit"] += 1
            return tok, self.cache_ms
        tok = Token(assertion.subject, audience, now, min(now + self.ttl, assertion.expires + self.ttl),
                    actor=self.actor, scopes=tuple(self.scopes.get(audience, ("read",))))
        self.cache[key] = tok
        self.stats["exchanged"] += 1
        return tok, self.exchange_ms


# ---------------------------------------------------------------- the turn contract and the mode flag
@dataclass(frozen=True)
class TurnRequest:
    turn_id: str
    conversation_id: str
    surface_version: str
    text: str
    assertion: Token


@dataclass
class TurnResponse:
    turn_id: str
    mode: str
    answer: str | None
    citations: list = field(default_factory=list)
    partial: list = field(default_factory=list)
    verification: str = ""
    audit_id: str = ""


class ModeFlag:
    """Server-side flag. The brain reads it on every turn; a surface may cache its own copy, so the brain decides."""

    def __init__(self, mode="live", ttl_s=30.0):
        if mode not in MODES:
            raise ValueError(mode)
        self.history = [(0.0, mode, "initial")]
        self.ttl = ttl_s

    def set(self, mode, at, reason):
        if mode not in MODES:
            raise ValueError(mode)
        self.history.append((at, mode, reason))

    def mode_at(self, t):
        """Mode the brain enforces at time t; a change takes effect when the brain's config cache expires."""
        m = self.history[0][1]
        for at, mode, _ in self.history[1:]:
            if t >= at + self.ttl:
                m = mode
        return m
