"""fieldkit v5.3 (Chapter 45): the hiring rubric.

A loop is a list of rounds; each round probes competencies either by observing the candidate do the work
or by asking the candidate to describe it (self-report). The module checks that a loop observes every
competency at least twice, refuses scores for competencies a round did not probe or that carry no evidence,
writes the debrief from independent scores, and measures interviewer calibration. It also checks a take-home
against an agent-only baseline, scores a discovery role-play from its event log, grades a workflow
classification against a key and checks a spoken answer for the five moves. Deterministic; no model calls.
"""
from __future__ import annotations

import re
import statistics as st
from dataclasses import dataclass, field

COMPETENCIES = ("discovery", "decomposition", "build", "judgment", "communication")
OBSERVED, SELF_REPORT = "observed", "self-report"
MUST_HAVE = ("discovery", "judgment")          # median of 3 or more, or no hire
FLOOR = 2                                      # no competency median below this
MIN_OBSERVED = 2                               # rounds that must observe each competency
TAKEHOME_CAP_MIN = 180                         # the take-home that respects the candidate's time
ANCHORS = {
    "discovery": {1: "proposes a solution before the workflow is described",
                  2: "asks about the happy path only",
                  3: "finds most paths and at least two exceptions, confirms back",
                  4: "finds the exceptions and who decides them, names what is still unknown"},
    "decomposition": {1: "one box called the model",
                      2: "steps listed, no interfaces",
                      3: "steps with inputs, outputs and an owner",
                      4: "steps ordered by risk, with the first thing to prove named"},
    "build": {1: "cannot get a working change in the time",
              2: "works on the happy path only",
              3: "working, tested change with the failure handled",
              4: "working change, test for the failure, and a note on what was not built"},
    "judgment": {1: "accepts the constraint or ignores it",
                 2: "names the constraint, no trade-off",
                 3: "states the trade-off and picks one with a reason",
                 4: "picks one, says what would change the decision and who signs"},
    "communication": {1: "talks past the listener",
                      2: "accurate but pitched at engineers only",
                      3: "pitched to the listener, answers the question asked",
                      4: "pitched to the listener, with a number and a next step they can act on"},
}


@dataclass(frozen=True)
class Probe:
    competency: str
    mode: str = OBSERVED

    def __post_init__(self):
        assert self.competency in COMPETENCIES, self.competency
        assert self.mode in (OBSERVED, SELF_REPORT), self.mode


@dataclass(frozen=True)
class Round:
    id: str
    name: str
    minutes: int
    probes: tuple
    takehome: bool = False

    def observes(self, c):
        return any(p.competency == c and p.mode == OBSERVED for p in self.probes)

    def asks(self, c):
        return any(p.competency == c for p in self.probes)


@dataclass
class Loop:
    name: str
    rounds: list

    def round(self, rid):
        return next(r for r in self.rounds if r.id == rid)

    def coverage(self):
        out = {}
        for c in COMPETENCIES:
            out[c] = {OBSERVED: [r.id for r in self.rounds if r.observes(c)],
                      SELF_REPORT: [r.id for r in self.rounds if r.asks(c) and not r.observes(c)]}
        return out

    def concentration(self):
        """Share of observed probes that land on the most-observed competency."""
        obs = [p.competency for r in self.rounds for p in r.probes if p.mode == OBSERVED]
        if not obs:
            return ("none", 0.0)
        top = max(COMPETENCIES, key=obs.count)
        return top, round(obs.count(top) / len(obs), 2)

    def minutes(self):
        live = sum(r.minutes for r in self.rounds if not r.takehome)
        home = sum(r.minutes for r in self.rounds if r.takehome)
        return live, home


@dataclass(frozen=True)
class Finding:
    code: str
    text: str


def lint_loop(loop, min_observed=MIN_OBSERVED, max_probes=2, cap=TAKEHOME_CAP_MIN):
    f, cov = [], loop.coverage()
    for c in COMPETENCIES:
        n = len(cov[c][OBSERVED])
        if n == 0:
            how = f"self-report only in {','.join(cov[c][SELF_REPORT])}" if cov[c][SELF_REPORT] else "not asked"
            f.append(Finding("L1", f"{c} never observed ({how})"))
        elif n < min_observed:
            f.append(Finding("L2", f"{c} observed in {n} round, needs {min_observed}"))
    top, share = loop.concentration()
    rounds_top = len(cov[top][OBSERVED]) if top != "none" else 0
    if rounds_top * 2 > len(loop.rounds):
        f.append(Finding("L3", f"{top} observed in {rounds_top} of {len(loop.rounds)} rounds "
                               f"({share:.0%} of observed probes): the rounds test the same competency"))
    for r in loop.rounds:
        if len(r.probes) > max_probes:
            f.append(Finding("L4", f"{r.id} probes {len(r.probes)} competencies in {r.minutes} min, max {max_probes}"))
        if r.takehome and r.minutes > cap:
            f.append(Finding("L5", f"{r.id} take-home is {r.minutes} min, cap {cap}"))
    return f


@dataclass(frozen=True)
class Score:
    interviewer: str
    round: str
    competency: str
    value: int
    evidence: str
    before_debrief: bool = True


class ScoreRefused(ValueError):
    pass


def check_score(loop, s):
    r = loop.round(s.round)
    if s.value not in (1, 2, 3, 4):
        raise ScoreRefused(f"{s.interviewer}/{s.round}/{s.competency}: value {s.value} not on the 1-4 scale")
    if not r.asks(s.competency):
        raise ScoreRefused(f"{s.interviewer}/{s.round}/{s.competency}: round did not probe it")
    if len(s.evidence.split()) < 6:
        raise ScoreRefused(f"{s.interviewer}/{s.round}/{s.competency}: no evidence written")
    return s


@dataclass
class Debrief:
    candidate: str
    decision: str
    table: dict
    flags: list
    refused: list
    probes: list = field(default_factory=list)
    reasons: list = field(default_factory=list)


def debrief(loop, candidate, scores):
    """Write the debrief from independent scores. Late scores are kept but marked; refused scores are dropped."""
    ok, refused, flags = [], [], []
    for s in scores:
        try:
            ok.append(check_score(loop, s))
        except ScoreRefused as e:
            refused.append(str(e))
    table = {}
    for c in COMPETENCIES:
        obs = [s for s in ok if s.competency == c and loop.round(s.round).observes(c)]
        vals = [s.value for s in obs]
        late = [s for s in obs if not s.before_debrief]
        table[c] = dict(values=vals, median=(st.median(vals) if vals else None),
                        spread=(max(vals) - min(vals) if vals else None), n=len(vals), late=len(late))
        if vals and max(vals) - min(vals) >= 2:
            flags.append(f"SPLIT {c}: {vals}, read the evidence before discussing")
        if len(vals) < MIN_OBSERVED:
            flags.append(f"THIN {c}: {len(vals)} observed score(s)")
        if late:
            flags.append(f"LATE {c}: {len(late)} score(s) written after discussion began")
    reasons, probes = [], []
    for c in COMPETENCIES:
        t = table[c]
        if t["n"] < MIN_OBSERVED:
            probes.append(f"{c}: schedule a 30-minute observed probe")
    for c in MUST_HAVE:
        m = table[c]["median"]
        if m is not None and m < 3:
            reasons.append(f"{c} median {m} below 3 (must-have)")
    for c in COMPETENCIES:
        m = table[c]["median"]
        if m is not None and m < FLOOR:
            reasons.append(f"{c} median {m} below floor {FLOOR}")
    decision = "no hire" if reasons else ("more evidence" if probes else "hire")
    return Debrief(candidate, decision, table, flags, refused, probes, reasons)


def render_debrief(d):
    out = [f"debrief {d.candidate}"]
    for c in COMPETENCIES:
        t = d.table[c]
        med = "-" if t["median"] is None else f"{t['median']:.1f}"
        out.append(f"  {c:<14} scores {str(t['values']):<12} median {med:>3}  n {t['n']}")
    for r in d.refused:
        out.append(f"  REFUSED {r}")
    for f in d.flags:
        out.append(f"  {f}")
    for r in d.reasons:
        out.append(f"  reason: {r}")
    for p in d.probes:
        out.append(f"  probe: {p}")
    out.append(f"  decision: {d.decision}")
    return "\n".join(out)


def calibrate(ratings):
    """ratings: (interviewer, session, competency, value). Reference is the panel median per session and competency.
    Returns {interviewer: (mean offset, share of scores equal to the reference, n)}."""
    ref = {}
    for _, sess, c, v in ratings:
        ref.setdefault((sess, c), []).append(v)
    ref = {k: st.median(v) for k, v in ref.items()}
    out = {}
    for who in sorted({r[0] for r in ratings}):
        mine = [(v - ref[(s, c)]) for w, s, c, v in ratings if w == who]
        out[who] = (round(sum(mine) / len(mine), 2), round(sum(d == 0 for d in mine) / len(mine), 2), len(mine))
    return out


def exact_agreement(ratings):
    """Share of (session, competency) cells where every interviewer gave the same value."""
    cells = {}
    for _, s, c, v in ratings:
        cells.setdefault((s, c), set()).add(v)
    return round(sum(len(v) == 1 for v in cells.values()) / len(cells), 2)


def discovery_score(events, facts):
    """events: (minute, kind, fact or None), kind in question/confirm/solution. facts: {id: is_exception}."""
    found = {f for _, k, f in events if f and k in ("question", "confirm")}
    first_solution = min([m for m, k, _ in events if k == "solution"], default=None)
    q_before = sum(1 for m, k, _ in events if k == "question" and (first_solution is None or m < first_solution))
    exc = sum(1 for f in found if facts.get(f))
    confirms = sum(1 for _, k, _ in events if k == "confirm")
    n_exc = sum(facts.values())
    if first_solution is not None and first_solution < 10 and len(found) < len(facts) // 2:
        anchor = 1
    elif exc == 0:
        anchor = 2
    elif len(found) >= 0.8 * len(facts) and exc >= n_exc - 1 and confirms >= 2:
        anchor = 4
    elif exc >= 2 and confirms >= 1:
        anchor = 3
    else:
        anchor = 2
    return dict(facts=len(found), of=len(facts), exceptions=exc, of_exc=n_exc, first_solution=first_solution,
                questions_before=q_before, confirms=confirms, anchor=anchor)


LEVELS = ("deterministic", "rules", "small model", "frontier model", "human decision")


def classify_score(answers, key):
    """Grade a whiteboard classification. Over-modeled: a model where the key has code or rules.
    Unsafe: anything automated where the key has a human decision."""
    agree = over = under = unsafe = 0
    detail = []
    for step, want in key.items():
        got = answers[step]
        gi, wi = LEVELS.index(got), LEVELS.index(want)
        if got == want:
            agree += 1; mark = "ok"
        elif want == "human decision":
            unsafe += 1; mark = "UNSAFE"
        elif gi > wi and got in ("small model", "frontier model"):
            over += 1; mark = "over-modeled"
        else:
            under += 1; mark = "under"
        detail.append((step, want, got, mark))
    return dict(agree=agree, n=len(key), over=over, under=under, unsafe=unsafe, detail=detail)


def takehome_validity(items, bar=3.0):
    """items: (name, weight, agent_solvable). An agent-only submission is modeled as 4 on agent-solvable items and
    1 elsewhere. If that clears the bar, the take-home measures the agent, not the candidate."""
    assert abs(sum(w for _, w, _ in items) - 1) < 1e-9
    base = sum(w * (4 if a else 1) for _, w, a in items)
    return dict(agent_baseline=round(base, 2), bar=bar, valid=base < bar,
                judgment_weight=round(sum(w for _, w, a in items if not a), 2))


MOVES = ("position", "evidence", "example", "boundary", "proof")
_BOUND = re.compile(r"\b(stops being true|unless|does not hold|would not|wouldn't|breaks (when|if)|except|"
                    r"the limit|not true when|only when|only if)\b", re.I)
_PROOF = re.compile(r"\b(I would show|I'd show|I can show|show you|I would bring|I'd bring|open the)\b", re.I)
_EXAMPLE = re.compile(r"\b(at [A-Z][a-z]+|on day \d+|day \d+|for [A-Z][a-z]+)\b")
_HEDGE = re.compile(r"^(it depends|well|so|great question|there are many)", re.I)


def five_moves(answer):
    sents = [s.strip() for s in re.split(r"(?<=[.?])\s+", answer.strip()) if s.strip()]
    first = sents[0] if sents else ""
    found = {
        "position": bool(first) and len(first.split()) <= 30 and not _HEDGE.match(first),
        "evidence": bool(re.search(r"\d", answer)),
        "example": bool(_EXAMPLE.search(answer)),
        "boundary": bool(_BOUND.search(answer)),
        "proof": bool(_PROOF.search(answer)),
    }
    return found


ROUND_ALIASES = {"phone screen": "screen", "screen": "screen", "technical": "technical", "design": "technical",
                 "scenario": "scenario", "on-site": "on-site", "onsite": "on-site", "hiring manager": "hiring manager",
                 "hiring-manager": "hiring manager", "customer panel": "customer panel",
                 "client simulation": "customer panel", "principal": "principal level", "senior": "principal level"}


def normalize_round(tag):
    return ROUND_ALIASES.get(tag.strip().lower(), "other")
