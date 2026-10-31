"""fieldkit v1: discovery notes as structured data (Chapter 6).

Written here first and promoted into 04-code/fieldkit/fieldkit/discovery.py once the chapter's tests pass.

A discovery note is one statement about one intake path, answering one of the five questions, from one kind
of source, on one day. The module keeps three rules the chapter argues for:

  1. Stated is not observed. Interviews and the written procedure are statements; shadowing and tracer
     documents are observations; system reports (artifacts) are evidence for counts and dates only.
  2. A path is covered only when every one of the five questions has evidence of the right kind and no
     contradiction on the path is open.
  3. A contradiction between what was stated and what was observed is a finding, not noise. It stays open
     until a named person resolves it on a named day.

Notes never hold customer data: the validator rejects text that looks like an identifier.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

LAYER = "v1"
STATED = ("interview", "procedure")
OBSERVED = ("shadow", "tracer")
EVIDENCE = OBSERVED + ("artifact",)
SOURCES = STATED + EVIDENCE
QUESTIONS = {
    "arrive": "What arrives, through which door, and how many?",
    "touch": "Who touches it, in what order, in which system?",
    "decide": "What is decided at each touch, and on what?",
    "except": "What happens when it does not fit?",
    "land": "Where does it land, and when is it done?",
}
# A report can say how many and when; only watching can say who, why and what happens when it does not fit.
ARTIFACT_OK = ("arrive", "land")
IDENTIFIER_PATTERNS = (r"\bHP[0-9A-Z]{5,}", r"\bCM-\d", r"\bMRN\b", r"\bDOB\b", r"\b\d{3}-\d{2}-\d{4}\b")


class NoteRejected(ValueError):
    pass


@dataclass
class Note:
    day: int
    source: str
    who: str
    path: str
    question: str
    text: str
    attribute: str | None = None
    value: float | None = None
    n: int = 0
    ref: str = ""

    def __post_init__(self):
        if self.source not in SOURCES:
            raise NoteRejected(f"unknown source {self.source!r}")
        if self.question not in QUESTIONS:
            raise NoteRejected(f"unknown question {self.question!r}")
        if self.source in OBSERVED and self.n < 1:
            raise NoteRejected(f"{self.path}: an observation needs a count of documents seen (n >= 1)")
        if (self.attribute is None) != (self.value is None):
            raise NoteRejected(f"{self.path}: attribute and value come together")
        if not self.who:
            raise NoteRejected(f"{self.path}: a note needs a person or document behind it")
        for pat in IDENTIFIER_PATTERNS:
            if re.search(pat, self.text):
                raise NoteRejected(f"{self.path}: note text looks like it holds an identifier ({pat})")


@dataclass
class Contradiction:
    path: str
    attribute: str
    stated: list
    observed: list
    stated_value: float
    observed_value: float
    resolved_by: str = ""
    resolved_day: int | None = None
    resolution: str = ""

    @property
    def open(self):
        return not self.resolved_by

    def render(self):
        s = "; ".join(f"{x.who} ({x.source}, day {x.day})" for x in self.stated)
        n = sum(x.n for x in self.observed)
        o = "; ".join(sorted({f"{x.who} ({x.source}, day {x.day})" for x in self.observed}))
        head = f"CONTRADICTION {self.path} {self.attribute}: stated {self.stated_value:g} by {s}"
        body = f"    observed {self.observed_value:.1f} over {n} documents: {o}"
        tail = (f"    resolved day {self.resolved_day} by {self.resolved_by}: {self.resolution}" if not self.open
                else "    open: path cannot be counted as covered")
        return "\n".join([head, body, tail])


@dataclass
class PathStatus:
    path: str
    name: str
    documented: bool
    volume: float | None
    marks: dict
    contradicted: bool
    seen: int = 0

    @property
    def covered(self):
        return all(m == "O" for m in self.marks.values()) and not self.contradicted


@dataclass
class CoverageReport:
    customer: str
    day: int
    rows: list
    contradictions: list

    @property
    def total_volume(self):
        return sum(r.volume or 0 for r in self.rows)

    @property
    def covered_volume(self):
        return sum(r.volume or 0 for r in self.rows if r.covered)

    def render(self):
        known = len(self.rows); doc = sum(r.documented for r in self.rows)
        out = [f"coverage report: {self.customer}, day {self.day}",
               f"paths known: {known} (documented {doc}, found {known - doc})",
               "path  doc  vol/mo  seen  arrive touch decide except land   status"]
        for r in self.rows:
            vol = f"{r.volume:,.0f}" if r.volume is not None else "?"
            m = "  ".join(f"{r.marks[q]:^5}" for q in QUESTIONS)
            st = "covered" if r.covered else ("contradicted" if r.contradicted else "open")
            out.append(f"{r.path:<5} {'yes' if r.documented else 'no':<4} {vol:>6}  {r.seen:>4}  {m}  {st}")
        cov = sum(r.covered for r in self.rows)
        unknown = [r.path for r in self.rows if r.volume is None]
        tv = self.total_volume
        share = f"{100 * self.covered_volume / tv:.1f}%" if tv else "n/a"
        out.append(f"covered: {cov} of {known} paths, {self.covered_volume:,.0f} of {tv:,.0f} documents a month ({share})")
        if unknown:
            out.append(f"volume unknown: {', '.join(unknown)}")
        stated = sum(m == "s" for r in self.rows for m in r.marks.values())
        out.append(f"answers stated but not observed: {stated}")
        opened = [c for c in self.contradictions if c.open]
        out.append(f"open contradictions: {len(opened)}")
        return "\n".join(out)


class DiscoveryLog:
    """Every discovery note for one customer, and the reports derived from them."""

    def __init__(self, customer, names=None, documented=()):
        self.customer = customer
        self.names = dict(names or {})
        self.documented = set(documented)
        self.notes: list[Note] = []
        self.resolutions: dict = {}

    def add(self, *notes):
        for n in notes:
            self.notes.append(n)
        return self

    def upto(self, day):
        return [n for n in self.notes if day is None or n.day <= day]

    def paths(self, day=None):
        seen = []
        for n in sorted(self.upto(day), key=lambda x: x.day):
            if n.path not in seen:
                seen.append(n.path)
        return sorted(seen)

    def first_seen(self, path):
        ns = sorted((n for n in self.notes if n.path == path), key=lambda x: (x.day, SOURCES.index(x.source)))
        return ns[0] if ns else None

    def mark(self, path, q, day=None):
        ns = [n for n in self.upto(day) if n.path == path and n.question == q]
        if any(n.source in OBSERVED for n in ns):
            return "O"
        if q in ARTIFACT_OK and any(n.source == "artifact" for n in ns):
            return "O"
        if any(n.source == "artifact" for n in ns):
            return "a"
        if ns:
            return "s"
        return "."

    def seen(self, path, day=None):
        """Documents actually watched on this path (largest count per observation session)."""
        per = {}
        for n in self.upto(day):
            if n.path == path and n.source in OBSERVED:
                per[n.ref or (n.day, n.who)] = max(per.get(n.ref or (n.day, n.who), 0), n.n)
        return sum(per.values())

    def volume(self, path, day=None):
        ns = [n for n in self.upto(day) if n.path == path and n.attribute == "monthly_volume"
              and n.source in EVIDENCE]
        return ns[-1].value if ns else None

    def resolve(self, path, attribute, by, day, resolution):
        if not by:
            raise ValueError("a contradiction is resolved by a named person")
        self.resolutions[(path, attribute)] = (by, day, resolution)

    def contradictions(self, day=None, tolerance=0.25):
        out = []
        ns = self.upto(day)
        keys = sorted({(n.path, n.attribute) for n in ns if n.attribute and n.attribute != "monthly_volume"})
        for path, attr in keys:
            st = [n for n in ns if n.path == path and n.attribute == attr and n.source in STATED]
            ob = [n for n in ns if n.path == path and n.attribute == attr and n.source in EVIDENCE]
            if not st or not ob:
                continue
            sv = st[-1].value
            w = sum(max(n.n, 1) for n in ob)
            ov = sum(n.value * max(n.n, 1) for n in ob) / w
            scale = max(abs(sv), abs(ov), 1.0)
            if abs(ov - sv) / scale > tolerance:
                c = Contradiction(path, attr, st, ob, sv, ov)
                r = self.resolutions.get((path, attr))
                if r and (day is None or r[1] <= day):
                    c.resolved_by, c.resolved_day, c.resolution = r
                out.append(c)
        return out

    def coverage(self, day=None, tolerance=0.25):
        cons = self.contradictions(day, tolerance)
        bad = {c.path for c in cons if c.open}
        rows = [PathStatus(p, self.names.get(p, p), p in self.documented, self.volume(p, day),
                           {q: self.mark(p, q, day) for q in QUESTIONS}, p in bad, self.seen(p, day))
                for p in self.paths(day)]
        last = max((n.day for n in self.upto(day)), default=0)
        return CoverageReport(self.customer, day if day is not None else last, rows, cons)


def naive_coverage(log, day=None):
    """What a team reports when it counts every answer, however it was obtained."""
    ps = log.paths(day)
    answered = [p for p in ps if all(log.mark(p, q, day) != "." for q in QUESTIONS)]
    return f"naive: {len(answered)} of {len(ps)} paths answered on all five questions ({100 * len(answered) / max(len(ps), 1):.0f}%)"


@dataclass
class Step:
    name: str
    path: str
    needs: tuple
    done_by: str


def permission_gaps(steps, roles, runs_as):
    """Steps the automation would perform under `runs_as` that need a permission that role does not hold."""
    have = set(roles[runs_as])
    gaps = []
    for s in steps:
        missing = [p for p in s.needs if p not in have]
        if missing:
            holders = sorted(r for r, ps in roles.items() if all(m in ps for m in missing))
            gaps.append((s, missing, holders))
    return gaps
