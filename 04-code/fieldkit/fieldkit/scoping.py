"""fieldkit.scoping: the scoping document as code (Chapter 8, book layer v1.2; package version unchanged).

A scoping document is a set of claims. Every claim carries one of five statuses, saying what it rests on:

    F  direct customer fact          a named person at the customer said it, on a stated day, in their words
    R  reconstructed from an artifact we read it in something the customer owns (a report, a procedure, a log)
    V  vendor position               we said it (a proposal, a deal sheet, a sales promise)
    P  proposed design               we propose it; nobody at the customer has accepted it yet
    D  decision required             nobody has decided it; it has one named owner and a due day

The one rule the lint exists for: a status never rises because a claim was repeated. A claim copied into a
later document keeps the status of its origin unless an evidence event (a named customer person, a day, an
artifact, their words) is attached at the step where it rises.

Numbers inside claims carry a basis (measured, estimated, assumed). The basis qualifies the number; the status
qualifies the claim. "Estimated, vendor position" is a common and honest combination.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .deployment import is_person
from .cadence import Record, Register

STATUS = {"F": "direct customer fact", "R": "reconstructed from an artifact", "V": "vendor position",
          "P": "proposed design", "D": "decision required"}
RANK = {"D": 0, "V": 1, "P": 1, "R": 2, "F": 3}          # what a claim may be relied on for
BASIS = ("measured", "estimated", "assumed", "target")      # a target is a bar, not a description
_NUMBER = re.compile(r"(?<![A-Z]-)(?<![\w.])\d[\d,.]*\s*(?:%|percent|minutes|hours|days|documents|a month|per)")


@dataclass(frozen=True)
class Source:
    who: str                 # a person, or the document's author
    party: str               # "customer" or "vendor"
    artifact: str            # the document, meeting or system the claim came from
    day: int                 # engagement day (negative before signature)


@dataclass(frozen=True)
class Evidence:
    who: str                 # the customer person who confirmed it
    day: int
    artifact: str
    words: str               # their words, verbatim, short


@dataclass
class Claim:
    key: str
    text: str
    status: str                              # one of STATUS
    source: Source
    section: str = ""
    basis: str | None = None                 # for claims that contain a number
    owner: str | None = None                 # for D
    due_day: int | None = None               # for D
    derived_from: str | None = None          # key of the claim this one repeats
    evidence: Evidence | None = None         # the event that justifies a rise in status


@dataclass
class Criterion:
    """A success criterion the customer signs and the evaluation suite enforces."""
    key: str
    statement: str
    metric: str = ""                         # what is counted, as a formula in words
    scorer: str = ""                         # a named person at the customer
    document_set: str = ""                   # named set
    set_size: int | None = None              # documents in it
    denominator: str = ""                    # what the percentage is of
    threshold: str = ""                      # the bar, with direction
    method: str = ""                         # the evaluation suite or script that measures it
    report: tuple = ()                       # lines reported separately, never averaged in

    def problems(self) -> list[tuple[str, str]]:
        out = []
        if not self.metric or not self.method:
            out.append(("NO MEASUREMENT", "nothing says what is counted or what counts it"))
        if not is_person(self.scorer):
            out.append(("NO SCORER", f"scorer {self.scorer or '(none)'!r} is not a named person"))
        if not self.document_set or not self.set_size:
            out.append(("NO DOCUMENT SET", "no named document set with a count"))
        if self.metric and not self.denominator:
            out.append(("NO DENOMINATOR", "a rate with nothing under it"))
        if not self.threshold:
            out.append(("NO THRESHOLD", "no bar, so no pass or fail"))
        return out


@dataclass
class DocType:
    key: str
    name: str
    decisions: tuple                         # decisions the system makes on it (keys of DECISIONS)
    volume: int                              # documents a month
    basis: str = "measured"


@dataclass
class Exclusion:
    item: str
    reason: str
    route: str                               # where it goes instead; never blank
    volume: int = 0
    revisit: str = ""                        # the open decision that could bring it in, if any


@dataclass
class OpenDecision:
    key: str
    question: str
    owner: str
    raised_day: int
    due_day: int | None
    impact: str                              # what moves if this is late or goes the other way
    options: tuple = ()
    kind: str = "design"
    register_key: str = ""                   # the engagement decision-register record it became

    def problems(self) -> list[tuple[str, str]]:
        out = []
        if not is_person(self.owner):
            out.append(("NO OWNER", f"owner {self.owner!r} is not a named person"))
        if self.due_day is None:
            out.append(("NO DUE DAY", "open with no due day"))
        if not self.impact:
            out.append(("NO IMPACT", "nothing says what moves if it is late"))
        return out


@dataclass
class ScopeDoc:
    customer: str
    day: int
    version: str
    doc_types: list
    decisions: dict                          # key -> what the system decides
    never: list                              # decisions the system never makes
    criteria: list
    exclusions: list
    register: list
    claims: list = field(default_factory=list)
    lineage: dict = field(default_factory=dict)  # claim key -> Claim, for claims in earlier documents
    signatories: tuple = ()

    # ------------------------------------------------------------------ the lint
    def origin(self, c: Claim) -> Claim:
        seen, cur = set(), c
        while cur.derived_from and cur.derived_from not in seen:
            seen.add(cur.key)
            nxt = self.lineage.get(cur.derived_from) or next((x for x in self.claims if x.key == cur.derived_from), None)
            if nxt is None:
                break
            cur = nxt
        return cur

    def chain(self, c: Claim) -> list:
        out, cur = [c], c
        while cur.derived_from:
            cur = self.lineage.get(cur.derived_from) or next((x for x in self.claims if x.key == cur.derived_from), None)
            if cur is None:
                break
            out.append(cur)
        return out[::-1]

    def claim_problems(self, c: Claim) -> list[tuple[str, str]]:
        out = []
        if c.status not in STATUS:
            return [("BAD STATUS", f"{c.status!r}")]
        if c.status == "F" and not (is_person(c.source.who) and c.source.party == "customer"
                                    and c.source.who != self.customer):
            out.append(("FACT WITHOUT A PERSON", f"source {c.source.who!r} ({c.source.party})"))
        if c.status == "R" and c.source.party != "customer":
            out.append(("RECONSTRUCTED FROM OUR OWN DOCUMENT", f"artifact {c.source.artifact!r} is the vendor's"))
        if c.status == "D" and (not is_person(c.owner or "") or c.due_day is None):
            out.append(("DECISION WITHOUT OWNER AND DATE", f"owner {c.owner!r}, due {c.due_day}"))
        if c.status == "D" and not any(d.key == c.key or d.register_key == c.key for d in self.register):
            if not any(c.key in d.question or c.key == d.key for d in self.register):
                out.append(("NOT IN REGISTER", "decision required but no open-decision record"))
        if _NUMBER.search(c.text) and c.basis not in BASIS:
            out.append(("NUMBER WITHOUT BASIS", "say measured, estimated, assumed or target"))
        # upgraded by repetition: walk the chain, flag each rise without an evidence event at that step
        ch = self.chain(c)
        for prev, nxt in zip(ch, ch[1:]):
            if RANK[nxt.status] > RANK[prev.status]:
                ev = nxt.evidence
                if ev is None or not is_person(ev.who) or not ev.words:
                    out.append(("UPGRADED BY REPETITION",
                                f"{prev.key} {STATUS[prev.status]} -> {nxt.key} {STATUS[nxt.status]} "
                                f"({nxt.source.artifact}, day {nxt.source.day}) with no evidence event"))
        return out

    def lint(self) -> list[tuple[str, str, str]]:
        out = []
        for cr in self.criteria:
            out += [(cr.key, code, msg) for code, msg in cr.problems()]
        for c in self.claims:
            out += [(c.key, code, msg) for code, msg in self.claim_problems(c)]
        for d in self.register:
            out += [(d.key, code, msg) for code, msg in d.problems()]
        for e in self.exclusions:
            if not e.route:
                out.append((e.item, "NO ROUTE", "excluded with nowhere to go"))
        if not self.never:
            out.append(("scope", "NO NEVER LIST", "nothing says what the system will never decide"))
        return out

    # ------------------------------------------------------------------ views
    def strip(self, section: str) -> str:
        order = "FRVPD"
        cs = sorted((c for c in self.claims if c.section == section), key=lambda c: order.index(c.status))
        return "".join(c.status for c in cs)

    def counts(self) -> dict:
        return {s: sum(c.status == s for c in self.claims) for s in "FRVPD"}

    def coverage(self) -> tuple[int, int]:
        inside = sum(t.volume for t in self.doc_types)
        return inside, inside + sum(e.volume for e in self.exclusions)

    def to_register(self):
        """The open decisions as engagement decision-register records (fieldkit.cadence, Chapter 13)."""
        reg = Register(self.customer)
        for d in self.register:
            reg.add(Record(d.register_key or d.key, d.question, d.owner, d.raised_day, d.due_day,
                           kind=d.kind, options=list(d.options), impact=d.impact))
        return reg

    def suite_config(self) -> list[dict]:
        """What the evaluation suite enforces: one entry per criterion, nothing the document does not say."""
        return [dict(key=c.key, metric=c.metric, scorer=c.scorer, set=c.document_set, n=c.set_size,
                     denominator=c.denominator, threshold=c.threshold, report=list(c.report), method=c.method)
                for c in self.criteria if not c.problems()]
