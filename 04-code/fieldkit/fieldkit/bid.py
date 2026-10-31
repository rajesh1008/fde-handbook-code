"""fieldkit.bid (book layer v1.5, Chapter 12): the engineering half of a bid as data.

What it holds:
  Question       an RFP question and the owner the bid manager routed it to
  triage         routes questions to engineering, joint or sales and flags engineering content routed to sales
  Standard       one line of the customer's platform standards with the bid's outcome and its evidence
  crosswalk      counts outcomes; refuses compliance on vendor say-so and deviations with no named approver
  Clarification  a written answer from the customer's clarification log and the fact it settles
  extract        finds commitments and estate claims in a response, with their claim status
  lint           the response rules; the one that matters most: no clarification may contradict a claim
  five_moves     checks an oral answer for position, evidence, worked example, boundary and proof
  safety_net     the one page taken into the oral defense
  to_register    moves every commitment engineering must later deliver into the open-decision register
No model calls. Deterministic, standard library only (plus fieldkit.scoping, cadence and deployment).
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field

from .cadence import Record, Register
from .deployment import is_person
from .scoping import STATUS

LAYER = "v1.5"
CUSTOMER_SOURCED = ("F", "R")
OWNERS = ("engineering", "joint", "sales")
ENG_TAGS = {"architecture", "integration", "security", "identity", "data", "model", "evaluation",
            "monitoring", "operations", "exit", "platform", "delivery"}
SALES_TAGS = {"price", "terms", "company", "references", "liability", "insurance", "staffing-cost"}


# ------------------------------------------------------------------------------------------------ triage
@dataclass
class Question:
    key: str
    section: str
    text: str
    tags: tuple = ()
    routed_to: str = ""


def owner_of(q: Question) -> str:
    e, s = bool(set(q.tags) & ENG_TAGS), bool(set(q.tags) & SALES_TAGS)
    return "joint" if e and s else "engineering" if e else "sales"


def triage(questions):
    """Counts by owner and section, and the misroutes: engineering content sent to sales alone."""
    counts = {o: 0 for o in OWNERS}
    by_section, misroutes = {}, []
    for q in questions:
        o = owner_of(q)
        counts[o] += 1
        by_section.setdefault(q.section, {k: 0 for k in OWNERS})[o] += 1
        if o != "sales" and q.routed_to == "sales":
            misroutes.append((q.key, o, q.text))
    return counts, by_section, misroutes


# ------------------------------------------------------------------------------------------------ standards
STD_OUTCOMES = ("comply", "comply with configuration", "deviation requested", "not applicable")


@dataclass
class Standard:
    key: str
    area: str
    text: str
    outcome: str
    evidence: str = ""
    evidence_status: str = "V"
    names_customer_system: bool = False
    approver: str = ""


def crosswalk(standards):
    counts = {o: 0 for o in STD_OUTCOMES}
    problems = []
    for s in standards:
        if s.outcome not in STD_OUTCOMES:
            problems.append((s.key, "UNKNOWN OUTCOME", s.outcome)); continue
        counts[s.outcome] += 1
        if s.outcome.startswith("comply"):
            if not s.evidence:
                problems.append((s.key, "NO EVIDENCE", "a compliance claim with nothing behind it"))
            elif s.names_customer_system and s.evidence_status not in CUSTOMER_SOURCED:
                problems.append((s.key, "COMPLY ON VENDOR SAY-SO",
                                 f"names a customer system; evidence is a {STATUS[s.evidence_status]}"))
        if s.outcome == "deviation requested" and not is_person(s.approver):
            problems.append((s.key, "DEVIATION WITHOUT APPROVER", f"approver {s.approver!r} is not a named person"))
    return counts, problems


# ------------------------------------------------------------------------------------------------ claims
@dataclass
class Clarification:
    key: str
    question: str
    answer: str
    subject: tuple = ()
    attribute: tuple = ()
    holds: bool = True
    round: int = 1


@dataclass
class Claim:
    key: str
    answer: str
    text: str
    kind: str          # estate | commitment
    status: str        # F R V P D, or "" if untagged
    source: str
    has_number: bool
    system: str
    flags: list = field(default_factory=list)


_TAG = re.compile(r"\s*\[(F|R|V|P|D)(?::\s*([^\]]*))?\]\.?\s*$")
_SPLIT = re.compile(r"(?<=[.\]])\s+(?=[A-Z])")
_COMMIT = re.compile(r"\b(?:we|Northlight) will\b|\bwill\b|\bwithin \d|\b\d[\d,.]*\s?(?:%|days?|weeks?|hours?|"
                     r"minutes?|seconds?|memos?|documents?)\b", re.I)
_VERBS = r"supports?|provides?|runs?|holds?|has|is|are|accepts?|raises?|exposes?|streams?|allows?|does|keeps?"


def _estate(customer):
    return re.compile(rf"\b(?:{re.escape(customer)}(?:'s)?|the bank(?:'s)?|your)\b.*?\b(?:{_VERBS})\b", re.I)
_NUMBER = re.compile(r"\b\d[\d,.]*\s?(?:%|days?|weeks?|hours?|minutes?|seconds?|memos?|documents?)?\b")
_SYSTEM = re.compile(r"\b(gateway|SIEM|directory|origination system|document store|productivity suite|change board)\b",
                     re.I)
_NEG = re.compile(r"\b(?:not|no|cannot|never|without)\b|n't\b", re.I)
_EXCLUDES = re.compile(r"\b(?:excluding|except|outside)\b", re.I)
_CONDITIONAL = re.compile(r"^(?:If|When|Should|Unless)\b")
_ORAL = re.compile(r"\b(?:conference|call|meeting|workshop|demo)\b", re.I)


def sentences(text: str):
    return [s.strip() for s in _SPLIT.split(" ".join(text.split())) if s.strip()]


def extract(answers: dict, customer: str = "Harbourline"):
    """answers: answer key -> response text. Returns the claims, numbered in order of appearance."""
    out, n, estate = [], 0, _estate(customer)
    for akey, text in answers.items():
        for s in sentences(text):
            m = _TAG.search(s)
            status, source = (m.group(1), (m.group(2) or "").strip()) if m else ("", "")
            body = _TAG.sub("", s).rstrip(".") + "." if m else s
            if estate.search(body) and not re.search(r"\bwill\b", body):
                kind = "estate"
            elif _COMMIT.search(body):
                kind = "commitment"
            else:
                continue
            n += 1
            sysm = _SYSTEM.search(body)
            out.append(Claim(f"BC-{n:02d}", akey, body, kind, status, source,
                             bool(_NUMBER.search(body)), sysm.group(1) if sysm else ""))
    return out


def lint(claims, clarifications=(), written_only=True):
    """Returns (claim key, level, code, message). ERROR blocks submission; WARN needs a written reason."""
    out = []
    def flag(c, level, code, msg):
        c.flags.append(code); out.append((c.key, level, code, msg))
    for c in claims:
        if c.kind == "estate":
            if not c.status:
                flag(c, "ERROR", "ESTATE CLAIM WITHOUT SOURCE", "every sentence about the customer's estate needs a "
                     "source the customer wrote")
            elif c.status not in CUSTOMER_SOURCED:
                flag(c, "ERROR", "ESTATE CLAIM WITH VENDOR STATUS",
                     f"a {STATUS[c.status]} written as a fact about the customer's estate")
        elif not c.status:
            flag(c, "WARN", "UNTAGGED COMMITMENT", "give it a status")
        if c.status == "F":
            who = c.source.split(",")[0].strip()
            if not is_person(who):
                flag(c, "ERROR", "FACT WITHOUT A NAMED PERSON", f"source {c.source!r}")
            elif written_only and _ORAL.search(c.source):
                flag(c, "WARN", "ORAL FACT", "the RFP says only the written clarification log binds")
        if c.status == "D":
            who = c.source.split(",")[0].strip()
            if not is_person(who) or not re.search(r"day \d+", c.source):
                flag(c, "ERROR", "DECISION WITHOUT OWNER OR DUE DAY", f"source {c.source!r}")
        if (c.kind == "commitment" and c.has_number and c.system and c.status not in CUSTOMER_SOURCED
                and not _EXCLUDES.search(c.text)):
            flag(c, "WARN", "NUMBER DEPENDS ON CUSTOMER SYSTEM",
                 f"the number rests on the customer's {c.system}; no customer source for it")
        if not _CONDITIONAL.match(c.text):
            low = c.text.lower()
            for k in clarifications:
                if k.subject and any(t in low for t in k.subject) and any(t in low for t in k.attribute):
                    asserted = not _NEG.search(c.text)
                    if asserted != k.holds:
                        flag(c, "ERROR", "CONTRADICTED", f"{k.key} (round {k.round}): {k.answer}")
    bad_answers = {c.answer for c in claims if "CONTRADICTED" in c.flags}
    for c in claims:
        if c.answer in bad_answers and "CONTRADICTED" not in c.flags and c.has_number and c.kind == "commitment":
            flag(c, "WARN", "AT RISK", f"a number in {c.answer}, an answer with a contradicted claim")
    return out


def strip(claims):
    """Status letters in order, for the claim-status strip (Signature 5)."""
    return "".join(c.status or "?" for c in claims)


# ------------------------------------------------------------------------------------------------ the oral defense
MOVES = ("position", "evidence", "example", "boundary", "proof")
_LIMIT = re.compile(r"\b(?:not|only|until|unless|outside|cannot|does not|will not)\b", re.I)
_ARTIFACT = re.compile(r"\b(?:log|register|report|output|listing|page|trace|test|record|file|crosswalk|minutes)\b",
                       re.I)


def five_moves(answer: dict, wpm: int = 150):
    """Missing or weak moves, and the spoken length in seconds at the given words per minute."""
    problems = [f"missing {m}" for m in MOVES if not answer.get(m, "").strip()]
    if answer.get("boundary") and not _LIMIT.search(answer["boundary"]):
        problems.append("boundary states no limit")
    if answer.get("proof") and not _ARTIFACT.search(answer["proof"]):
        problems.append("proof names no artifact the panel can keep")
    if answer.get("evidence") and not re.search(r"\d", answer["evidence"]):
        problems.append("evidence has no number")
    words = sum(len(answer.get(m, "").split()) for m in MOVES)
    return problems, round(words * 60 / wpm)


def safety_net(customer, claims, standards, not_promised, boundary, width=96, max_lines=60):
    """The one page. Every line comes from the response, the crosswalk or the register; nothing is new."""
    L = [f"{customer}: oral defense safety net (one page)", ""]
    nums = [c for c in claims if c.kind == "commitment" and c.has_number]
    L.append(f"Numbers we will defend ({len(nums)}), with status:")
    L += [f"  {c.key} [{c.status}] {c.text}" for c in nums]
    est = [c for c in claims if c.kind == "estate"]
    L.append(f"Statements about {customer}'s estate ({len(est)}), every one sourced to {customer}:")
    L += [f"  {c.key} [{c.source}] {c.text}" for c in est]
    L.append("Decisions that belong to " + customer + ":")
    L += [f"  {c.key} {c.source}: {c.text}" for c in claims if c.status == "D"]
    L.append("Deviations requested from platform standards:")
    L += [f"  {s.key} approver {s.approver}: {s.text}" for s in standards if s.outcome == "deviation requested"]
    L.append("We have not promised:")
    L += [f"  - {x}" for x in not_promised]
    L += ["The boundary sentence:", f"  {boundary}"]
    wrapped = []
    for line in L:
        while len(line) > width:
            cut = line.rfind(" ", 0, width)
            wrapped.append(line[:cut]); line = "      " + line[cut + 1:]
        wrapped.append(line)
    if len(wrapped) > max_lines:
        raise ValueError(f"safety net is {len(wrapped)} lines; the page holds {max_lines}")
    return wrapped


# ------------------------------------------------------------------------------------------------ after the award
def to_register(claims, register: Register, owner_for: dict, due_for: dict, raised_day: int = 0):
    """Every proposed design, decision required and vendor number becomes a record engineering must close."""
    moved = []
    for c in claims:
        if not (c.status in ("P", "D") or (c.status == "V" and c.has_number)):
            continue
        if c.status == "D":
            owner = c.source.split(",")[0].strip()
            due = int(re.search(r"day (\d+)", c.source).group(1))
        else:
            owner, due = owner_for.get(c.answer, ""), due_for.get(c.answer)
        r = register.add(Record(c.key, c.text, owner, raised_day, due, kind="bid",
                                evidence=f"{c.answer} [{c.status}]", impact=" ".join(c.flags)))
        moved.append(r)
    return moved
