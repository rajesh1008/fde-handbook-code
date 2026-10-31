"""fieldkit v3.2 (Chapter 25): agents that act in the customer's systems.

Five pieces, each small enough to read in one sitting:
  ReleaseBoundary  which levels (read, draft, write, background, memory) are granted, where, by whom, on which day
  Authorizer       a deterministic, per-call check in front of every action; deny by default
  Proposal         what the agent wants to do, bound to an intent key that survives retries
  ActionLedger     three joinable records (recommendation, human response, final outcome) plus one action record
                   per attempt, including denials and compensations
  Executor         propose -> authorize -> execute -> verify; the executor owns retries, never the model

Writing itself goes through connectors.WriteBack (v2.4), which already finds a key before writing again,
holds rejected writes and voids orphan shells."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict

LEVELS = ("read", "draft", "write", "background", "memory")


def digest(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:12]


def intent_key(prefix: str, source_id: str, op: str, version: int = 1) -> str:
    """The idempotency key belongs to the intent (this document, this operation), not to the call."""
    return f"{prefix}-{op}-{source_id}-v{version}"


# ---------------------------------------------------------------- release boundaries
@dataclass(frozen=True)
class Grant:
    level: str
    envs: tuple
    ops: tuple
    approved_by: str
    day: int
    condition: str = ""


class ReleaseBoundary:
    def __init__(self, customer, grants, refused=None):
        self.customer, self.grants = customer, list(grants)
        self.refused = dict(refused or {})          # op -> who refused it, kept visible on purpose
        for g in self.grants:
            assert g.level in LEVELS, g.level

    def grant_for(self, op, env):
        return next((g for g in self.grants if op in g.ops and env in g.envs), None)

    def check(self, op, env):
        if op in self.refused:
            return False, f"refused: {self.refused[op]}"
        g = self.grant_for(op, env)
        if g is None:
            return False, f"no grant for {op} in {env}"
        return True, f"{g.level} granted by {g.approved_by}, day {g.day}"

    def table(self):
        rows = []
        for lv in LEVELS:
            gs = [g for g in self.grants if g.level == lv]
            if not gs:
                rows.append(f"{lv:<10} not granted")
            for g in gs:
                rows.append(f"{lv:<10} {','.join(g.envs):<22} {g.approved_by:<16} day {g.day:<4} {g.condition}")
        rows += [f"refused    {op:<22} {who}" for op, who in self.refused.items()]
        return "\n".join(rows)


# ---------------------------------------------------------------- per-call authorization
@dataclass
class Proposal:
    intent: str
    op: str
    env: str
    args: dict
    source: str
    agent_version: str = ""
    narrative: str = ""             # the model's own words; never what the reviewer approves


@dataclass
class Decision:
    allowed: bool
    stage: str
    reasons: list
    needs_human: bool = False


class Authorizer:
    """Checks every call with its concrete values. Stages run in order; the first failure denies."""

    def __init__(self, boundary, protected=(), rules=(), human_for=("write",), key_prefix=""):
        self.b, self.protected, self.rules = boundary, set(protected), list(rules)
        self.human_for, self.key_prefix = set(human_for), key_prefix
        self.finals: dict[str, str] = {}             # intent -> the system of record's rejection

    def authorize(self, p: Proposal) -> Decision:
        ok, why = self.b.check(p.op, p.env)
        if not ok:
            return Decision(False, "boundary", [why])
        touched = sorted(self.protected & set(p.args))
        if touched:
            return Decision(False, "protected", [f"{touched} belong to the system of record"])
        if p.intent in self.finals:
            return Decision(False, "finality", [f"system of record said: {self.finals[p.intent]}"])
        failed = [r.rule_id for r in self.rules if not r.check(p.args)]
        if failed:
            return Decision(False, "values", failed)
        if not p.intent.startswith(self.key_prefix) or p.source not in p.intent:
            return Decision(False, "key", ["intent key not bound to the source document"])
        level = self.b.grant_for(p.op, p.env).level
        return Decision(True, "allowed", [why], needs_human=level in self.human_for)

    def record_final(self, intent, reason):
        self.finals[intent] = reason


# ---------------------------------------------------------------- the three records and the action log
@dataclass
class Recommendation:
    rec_id: str
    case: str
    payload: dict
    agent_version: str
    day: int


@dataclass
class Response:
    rec_id: str
    reviewer: str
    verdict: str                    # accepted | edited | rejected
    payload: dict | None
    seconds: int
    day: int


@dataclass
class Outcome:
    case: str
    source: str                     # where the final answer came from, e.g. the production extract
    payload: dict
    day: int


@dataclass
class ActionRecord:
    action_id: str
    intent: str
    op: str
    env: str
    identity: str
    stage: str
    reasons: list
    request_hash: str
    state: str                      # denied | awaiting | verified | held | unknown | compensated | routed
    target_id: str | None = None
    raw: list = field(default_factory=list)
    links: dict = field(default_factory=dict)
    day: int = 0


class ActionLedger:
    def __init__(self):
        self.recs: dict[str, Recommendation] = {}
        self.resps: dict[str, Response] = {}
        self.outs: dict[str, Outcome] = {}
        self.actions: list[ActionRecord] = []

    def recommend(self, r):
        assert r.rec_id not in self.recs, "a recommendation is written once and never edited"
        self.recs[r.rec_id] = r

    def respond(self, r):
        assert r.rec_id in self.recs and r.rec_id not in self.resps
        self.resps[r.rec_id] = r

    def outcome(self, o):
        self.outs[o.case] = o

    def act(self, a):
        self.actions.append(a)
        return a

    def join(self, fields):
        rows = []
        for rid, rec in self.recs.items():
            resp, out = self.resps.get(rid), self.outs.get(rec.case)
            same = (lambda a, b: a is not None and b is not None and all(a.get(f) == b.get(f) for f in fields))
            rows.append(dict(rec_id=rid, case=rec.case, verdict=resp.verdict if resp else "none",
                             rec_eq_out=same(rec.payload, out.payload if out else None),
                             resp_eq_out=same(resp.payload if resp else None, out.payload if out else None),
                             has_outcome=out is not None))
        return rows

    def scoreboard(self, fields):
        rows = self.join(fields)
        n = len(rows)
        c = lambda f: sum(1 for r in rows if f(r))
        return dict(recommendations=n,
                    accepted=c(lambda r: r["verdict"] == "accepted"),
                    edited=c(lambda r: r["verdict"] == "edited"),
                    rejected=c(lambda r: r["verdict"] == "rejected"),
                    with_outcome=c(lambda r: r["has_outcome"]),
                    rec_matches_outcome=c(lambda r: r["rec_eq_out"]),
                    accepted_but_outcome_differs=c(lambda r: r["verdict"] == "accepted" and not r["rec_eq_out"]
                                                   and r["has_outcome"]),
                    edit_matches_outcome=c(lambda r: r["verdict"] == "edited" and r["resp_eq_out"]))

    def by_state(self):
        out = {}
        for a in self.actions:
            out[a.state] = out.get(a.state, 0) + 1
        return dict(sorted(out.items()))


# ---------------------------------------------------------------- the executor
class Executor:
    """Propose, authorize, execute, verify. One intent key per intent; retries reuse it."""

    def __init__(self, writeback, authorizer, ledger, identity, env):
        self.wb, self.az, self.ledger, self.identity, self.env = writeback, authorizer, ledger, identity, env
        self.n = 0

    def _rec(self, p, d, state, e=None, day=0, links=None):
        self.n += 1
        return self.ledger.act(ActionRecord(f"A{self.n:05d}", p.intent, p.op, p.env, self.identity, d.stage,
                                            list(d.reasons), digest(p.args), state,
                                            e.target_id if e else None, list(e.reasons) if e else [],
                                            links or {}, day))

    def run(self, p: Proposal, approved_by: str | None = None, day=0):
        d = self.az.authorize(p)
        if not d.allowed:
            return self._rec(p, d, "denied", day=day)
        if d.needs_human and not approved_by:
            return self._rec(p, d, "awaiting", day=day)
        e = self.wb.submit(p.intent, p.args)
        if e.state == "held" and e.reasons and e.reasons[0].startswith("rejected"):
            self.az.record_final(p.intent, e.reasons[0])
        return self._rec(p, d, e.state, e, day, {"approved_by": approved_by} if approved_by else None)

    def compensate(self, target_id, survivor, touched_by=None, day=0):
        """Undo our own duplicate through the customer's own procedure, or hand it to a person."""
        p = Proposal(f"void-{target_id}", "void_duplicate", self.env, {"claim": target_id, "survivor": survivor},
                     target_id)
        if touched_by:
            return self._rec(p, Decision(False, "compensation", [f"touched by {touched_by}; route to a person"]),
                             "routed", day=day, links={"survivor": survivor})
        ok = self.wb.t.void(target_id)
        return self._rec(p, Decision(True, "compensation", ["untouched agent-created duplicate"]),
                         "compensated" if ok else "held", day=day, links={"survivor": survivor})


def render_review(payload: dict, document: dict, fields) -> list[str]:
    """The review screen is drawn from the payload that will be sent, next to the source document,
    never from the model's description of it."""
    out = []
    for f in fields:
        a, b = document.get(f), payload.get(f)
        out.append(f"{'  ' if a == b else '! '}{f:<11} document={a!s:<14} will write={b!s}")
    return out
