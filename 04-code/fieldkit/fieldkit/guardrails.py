"""fieldkit.guardrails (book layer v3.5, Chapter 28): the customer's rules as enforced, tested guardrails.

A customer's rules arrive as sentences: signed documents, regulations, payer tables and, most of all, things people
say in a room or do at a desk without ever writing them down. This module turns each sentence into something a
pipeline can enforce and a test can break:

- RuleCard: one rule with who stated it, who owns it, what kind it is (input, output, action, budget), what happens
  when it is violated (block, route, repair, flag) and its status (signed, VERIFY, retired). A card lints itself.
- Statement and elicitation_report: what was said in each session and what became of it (a rule, merged into a
  rule, out of scope, contradicted by a signed document).
- GuardrailSuite: runs every live rule of one kind against a context. A rule with no check, or a check that raises,
  fails closed. The strongest effect wins: block > route > repair > flag.
- RuleTest and test_rules: every rule needs at least one case it must pass and one it must catch; a rule without
  both is reported as untested, whatever its prose says.
- Budget, CircuitBreaker and FleetBreaker: step, tool-call, repeated-call, token and cost budgets as action
  guardrails; a breaker that opens after repeated calls that make no progress and fails closed to a person; a
  fleet breaker that pages the on-call when too many runs trip in one window.

The package version stays 0.1.0; v3.5 is the book layer.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable

KINDS = ("input", "output", "action", "budget")
SOURCES = ("signed", "boundary", "regulation", "payer", "session", "observed", "redteam", "engineering")
STATUSES = ("signed", "VERIFY", "retired")
EFFECTS = ("block", "route", "repair", "flag")
MODALITIES = ("prohibit", "oblige")
PRECEDENCE = {"pass": -1, "flag": 0, "repair": 1, "route": 2, "block": 3}


@dataclass(frozen=True)
class RuleCard:
    rid: str
    statement: str
    kind: str
    source: str
    owner: str
    stated_by: str
    day: int
    effect: str = "block"
    route_to: str = ""
    modality: str = "prohibit"
    enforcement: str = "deterministic"
    status: str = "signed"
    review_by: int | None = None
    since: str = "v1"

    def lint(self) -> list[str]:
        p = []
        if self.kind not in KINDS:
            p.append(f"{self.rid}: unknown kind {self.kind!r}")
        if self.source not in SOURCES:
            p.append(f"{self.rid}: unknown source {self.source!r}")
        if self.effect not in EFFECTS:
            p.append(f"{self.rid}: unknown effect {self.effect!r}")
        if self.modality not in MODALITIES:
            p.append(f"{self.rid}: unknown modality {self.modality!r}")
        if self.status not in STATUSES:
            p.append(f"{self.rid}: unknown status {self.status!r}")
        if not self.owner:
            p.append(f"{self.rid}: no owner")
        if not self.stated_by:
            p.append(f"{self.rid}: nobody stated it")
        if self.status == "VERIFY" and self.review_by is None:
            p.append(f"{self.rid}: VERIFY with no review day")
        if self.effect == "route" and not self.route_to:
            p.append(f"{self.rid}: routes to nobody")
        if self.modality == "oblige" and self.effect == "block" and not self.route_to:
            p.append(f"{self.rid}: an obligation that only blocks never says who completes it")
        return p


@dataclass(frozen=True)
class Statement:
    sid: str
    day: int
    session: str
    said_by: str
    text: str
    disposition: str  # "rule:R-ID", "merged:R-ID", "out of scope", "contradicted:<document>"


def elicitation_report(statements: list[Statement], cards: list[RuleCard]) -> dict:
    by_session = Counter(s.session for s in statements)
    disp = Counter(s.disposition.split(":")[0] for s in statements)
    rids = {c.rid for c in cards}
    dangling = [s.sid for s in statements if s.disposition.split(":")[0] in ("rule", "merged")
                and s.disposition.split(":", 1)[1] not in rids]
    from_sessions = {s.disposition.split(":", 1)[1] for s in statements if s.disposition.startswith("rule:")}
    return dict(statements=len(statements), by_session=dict(by_session), disposition=dict(disp),
                rules_from_statements=len(from_sessions), dangling=dangling)


@dataclass(frozen=True)
class Verdict:
    rid: str
    ok: bool
    effect: str
    reason: str = ""
    route_to: str = ""


@dataclass
class Decision:
    verdicts: list[Verdict]
    effect: str = "pass"
    route_to: str = ""

    @staticmethod
    def of(verdicts: list[Verdict]) -> "Decision":
        failed = [v for v in verdicts if not v.ok]
        if not failed:
            return Decision(verdicts, "pass", "")
        top = max(failed, key=lambda v: PRECEDENCE[v.effect])
        return Decision(verdicts, top.effect, top.route_to)

    @property
    def failed(self) -> list[Verdict]:
        return [v for v in self.verdicts if not v.ok]


Check = Callable[[dict], "tuple[bool, str]"]


class GuardrailSuite:
    """Runs the live rules of one kind. Missing checks and raising checks fail closed (block)."""

    def __init__(self, cards: list[RuleCard], checks: dict[str, Check], version: str = "v1"):
        self.cards = {c.rid: c for c in cards}
        self.checks = dict(checks)
        self.version = version

    def live(self, kind: str | None = None) -> list[RuleCard]:
        return [c for c in self.cards.values() if c.status != "retired" and (kind is None or c.kind == kind)]

    def missing(self) -> list[str]:
        return sorted(c.rid for c in self.live() if c.rid not in self.checks)

    def lint(self) -> list[str]:
        out = []
        for c in self.cards.values():
            out += c.lint()
        return out

    def check_one(self, rid: str, ctx: dict) -> Verdict:
        c = self.cards[rid]
        fn = self.checks.get(rid)
        if fn is None:
            return Verdict(rid, False, "block", "no check for this rule: fail closed", c.route_to)
        try:
            ok, reason = fn(ctx)
        except Exception as e:  # a broken check is a closed gate, never an open one
            return Verdict(rid, False, "block", f"check raised {type(e).__name__}: fail closed", c.route_to)
        return Verdict(rid, bool(ok), "pass" if ok else c.effect, reason, c.route_to if not ok else "")

    def run(self, kind: str, ctx: dict) -> Decision:
        return Decision.of([self.check_one(c.rid, ctx) for c in self.live(kind)])


@dataclass(frozen=True)
class RuleTest:
    rid: str
    name: str
    ctx: dict
    expect_ok: bool


@dataclass
class TestReport:
    results: list[tuple[RuleTest, bool]]
    untested: list[str]
    failures: list[str]

    @property
    def passed(self) -> int:
        return sum(1 for _, good in self.results if good)


def test_rules(suite: GuardrailSuite, tests: list[RuleTest]) -> TestReport:
    """Run each test against its own rule. A rule needs a case it passes and a case it catches."""
    results, has = [], defaultdict(set)
    for t in tests:
        if t.rid not in suite.cards:
            results.append((t, False))
            continue
        v = suite.check_one(t.rid, t.ctx)
        results.append((t, v.ok == t.expect_ok))
        has[t.rid].add(t.expect_ok)
    untested = sorted(c.rid for c in suite.live() if has[c.rid] != {True, False})
    failures = [f"{t.rid} {t.name}" for t, good in results if not good]
    return TestReport(results, untested, failures)


@dataclass
class Budget:
    """Action guardrails on the loop itself. charge() returns None, or the reason the run must stop."""
    max_steps: int = 12
    max_tool_calls: int = 20
    max_repeat: int = 2
    max_tokens: int = 60_000
    max_cost: float = 0.40
    steps: int = 0
    tool_calls: int = 0
    tokens: int = 0
    cost: float = 0.0
    seen: Counter = field(default_factory=Counter)

    def charge(self, tool: str | None = None, args: Any = None, tokens: int = 0, cost: float = 0.0) -> str | None:
        self.steps += 1
        self.tokens += tokens
        self.cost += cost
        if tool is not None:
            self.tool_calls += 1
            key = (tool, repr(sorted(args.items())) if isinstance(args, dict) else repr(args))
            self.seen[key] += 1
            if self.seen[key] > self.max_repeat:
                return f"repeat budget: {tool} called {self.seen[key]} times with the same arguments"
        if self.steps > self.max_steps:
            return f"step budget: {self.steps} steps > {self.max_steps}"
        if self.tool_calls > self.max_tool_calls:
            return f"tool-call budget: {self.tool_calls} > {self.max_tool_calls}"
        if self.tokens > self.max_tokens:
            return f"token budget: {self.tokens} > {self.max_tokens}"
        if self.cost > self.max_cost:
            return f"cost budget: ${self.cost:.3f} > ${self.max_cost:.2f}"
        return None


class CircuitBreaker:
    """Opens after `threshold` consecutive calls to one tool that make no progress. Open means: stop, hand to a person."""

    def __init__(self, threshold: int = 3):
        self.threshold = threshold
        self.no_progress: Counter = Counter()
        self.state: dict[str, str] = defaultdict(lambda: "closed")

    def record(self, tool: str, progress: bool) -> str:
        if self.state[tool] == "open":
            return "open"
        if progress:
            self.no_progress[tool] = 0
        else:
            self.no_progress[tool] += 1
            if self.no_progress[tool] >= self.threshold:
                self.state[tool] = "open"
        return self.state[tool]

    def allow(self, tool: str) -> bool:
        return self.state[tool] != "open"


class FleetBreaker:
    """Counts tripped runs per window; above `rate` of runs (with at least `min_runs`), it pages."""

    def __init__(self, rate: float = 0.05, min_runs: int = 20, page: str = ""):
        self.rate, self.min_runs, self.page = rate, min_runs, page
        self.windows: dict[str, list[int]] = defaultdict(lambda: [0, 0])

    def record(self, window: str, tripped: bool) -> str | None:
        w = self.windows[window]
        w[0] += 1
        w[1] += int(tripped)
        if w[0] >= self.min_runs and w[1] / w[0] > self.rate:
            return f"page {self.page}: {w[1]} of {w[0]} runs tripped in {window}"
        return None


def coverage_table(cards: list[RuleCard]) -> dict:
    """Counts by kind x enforcement, by source and by status, for the rule register."""
    live = [c for c in cards if c.status != "retired"]
    return dict(kind=Counter(c.kind for c in live),
                enforcement=Counter((c.kind, c.enforcement) for c in live),
                source=Counter(c.source for c in live), status=Counter(c.status for c in live),
                modality=Counter(c.modality for c in live), effect=Counter(c.effect for c in live))
