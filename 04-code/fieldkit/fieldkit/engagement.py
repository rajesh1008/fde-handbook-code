"""fieldkit v0: the engagement repository (Chapter 3).

An engagement is kept as a repository from day 1, not as a deck. Five kinds of record, each a plain file
the customer could read:

    notes/       what was said or seen, by whom, on which day, and what kind of statement it is
    decisions/   open questions with an owner and a due day, until somebody answers them
    access/      the requests (the access tracker arrives fully in Chapter 15; v0 keeps a simple list)
    evidence/    every number anyone will repeat: value, who measured it, on what, where the files are
    status/      the Friday status, generated from the four folders above, never typed by hand

The rule the module enforces: a sentence in the status must come from a record, and a number must come
from an evidence record that names its measurer and its documents.
"""
from __future__ import annotations

import json
import pathlib
import re
from dataclasses import asdict, dataclass, field

LAYER = "v0"
NOTE_KINDS = ("fact", "promise", "ask", "finding", "question", "plan")
EVIDENCE_KINDS = ("measured", "stand-in", "anecdote")
_NUMBER_WORDS = r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|all|every|none)\b"


def _days(n: int) -> str:
    return f"{n} day" if n == 1 else f"{n} days"


def _who(name: str) -> str:
    return name or "nobody named"


@dataclass
class Note:
    day: int
    author: str
    kind: str
    text: str
    source: str = ""          # "kickoff", "email", "architecture review", ...
    verifier: str = ""        # for a promise: who at the customer can check it
    closed_day: int | None = None

    def __post_init__(self):
        if self.kind not in NOTE_KINDS:
            raise ValueError(f"note kind must be one of {NOTE_KINDS}, got {self.kind!r}")


@dataclass
class Decision:
    key: str
    question: str
    owner: str
    raised_day: int
    due_day: int | None = None
    status: str = "open"      # open | decided | dropped
    answer: str = ""
    decided_day: int | None = None

    def age(self, today: int) -> int:
        end = self.decided_day if self.decided_day is not None else today
        return end - self.raised_day


@dataclass
class Request:
    key: str
    what: str
    owner: str                # the named person at the customer who can say yes
    requested_day: int
    status: str = "requested"  # requested | in review | granted | refused
    blocks: str = ""

    @property
    def open(self) -> bool:
        return self.status not in ("granted", "refused")


@dataclass
class Evidence:
    key: str
    claim: str                # the sentence people will repeat
    value: str
    measured_by: str          # a person, not a team
    on_what: str              # the documents, with a count
    day: int
    kind: str = "measured"
    location: str = ""        # where the scored files live; "deleted day N" is a valid answer
    caveat: str = ""

    def __post_init__(self):
        if self.kind not in EVIDENCE_KINDS:
            raise ValueError(f"evidence kind must be one of {EVIDENCE_KINDS}, got {self.kind!r}")


@dataclass
class EngagementRepo:
    customer: str
    notes: list[Note] = field(default_factory=list)
    decisions: list[Decision] = field(default_factory=list)
    requests: list[Request] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)

    # ---- recording -------------------------------------------------------------------------------
    def note(self, day, author, kind, text, **kw) -> Note:
        n = Note(day, author, kind, text, **kw)
        self.notes.append(n)
        return n

    def decision(self, key, question, owner, raised_day, due_day=None) -> Decision:
        d = Decision(key, question, owner, raised_day, due_day)
        self.decisions.append(d)
        return d

    def decide(self, key, day, answer) -> Decision:
        d = self._get(self.decisions, key)
        d.status, d.answer, d.decided_day = "decided", answer, day
        return d

    def request(self, key, what, owner, requested_day, status="requested", blocks="") -> Request:
        r = Request(key, what, owner, requested_day, status, blocks)
        self.requests.append(r)
        return r

    def measure(self, key, claim, value, measured_by, on_what, day, **kw) -> Evidence:
        e = Evidence(key, claim, value, measured_by, on_what, day, **kw)
        self.evidence.append(e)
        return e

    @staticmethod
    def _get(items, key):
        for it in items:
            if it.key == key:
                return it
        raise KeyError(key)

    # ---- checks ----------------------------------------------------------------------------------
    def lint(self, today: int) -> list[str]:
        """Problems a reviewer would find. Empty list means the repo can produce an honest status."""
        out = []
        for n in self.notes:
            if n.kind == "promise" and n.closed_day is None and not n.verifier:
                out.append(f"PROMISE-NO-VERIFIER day {n.day} {n.author}: {n.text}")
        for d in self.decisions:
            if d.status == "open" and not d.owner:
                out.append(f"DECISION-NO-OWNER {d.key}: {d.question}")
            if d.status == "open" and d.due_day is not None and today > d.due_day:
                out.append(f"DECISION-OVERDUE {d.key} (due day {d.due_day}, owner {d.owner})")
        for r in self.requests:
            if r.open and not r.owner:
                out.append(f"REQUEST-NO-OWNER {r.key}: {r.what}")
        for e in self.evidence:
            if not e.measured_by or not re.search(r"\d", e.on_what):
                out.append(f"EVIDENCE-UNSOURCED {e.key}: {e.claim}")
        return out

    def audit(self, lines: list[tuple[str, str | None]]) -> list[str]:
        """Check a hand-written status. Each line is (sentence, evidence key or None).

        A sentence that contains a number, a percentage or a word of measurement must cite evidence;
        a cited key must exist. Returns one verdict per line."""
        keys = {e.key: e for e in self.evidence}
        verdicts = []
        for text, key in lines:
            claims_measure = bool(re.search(r"\d|%|validated|accura|proven|tested|" + _NUMBER_WORDS, text, re.I))
            if key is None and claims_measure:
                verdicts.append(f"UNSUPPORTED  {text}")
            elif key is not None and key not in keys:
                verdicts.append(f"NO-SUCH-EVIDENCE ({key})  {text}")
            elif key is not None:
                e = keys[key]
                verdicts.append(f"CITES {key}: {e.value}, {e.measured_by}, {e.on_what}  {text}")
            else:
                verdicts.append(f"OK (no claim)  {text}")
        return verdicts

    # ---- status ----------------------------------------------------------------------------------
    def status(self, today: int) -> str:
        open_req = [r for r in self.requests if r.open]
        blockers = [r for r in open_req if r.blocks]
        findings = [n for n in self.notes if n.kind == "finding" and n.closed_day is None]
        open_dec = sorted((d for d in self.decisions if d.status == "open"), key=lambda d: -d.age(today))
        promises = [n for n in self.notes if n.kind == "promise" and n.closed_day is None]
        data_rungs = [r for r in self.requests if r.status == "granted" and "customer data" in r.what]
        lines = [f"# {self.customer}: status, day {today}", ""]
        head = (f"Headline: day {today}; customer data on any rung: {'yes' if data_rungs else 'none'}; "
                f"{len(blockers)} blocker{'s' if len(blockers) != 1 else ''}; "
                f"{len(findings)} open finding{'s' if len(findings) != 1 else ''}.")
        lines += [head, "", "Measured this week:"]
        for e in self.evidence:
            cav = f" Caveat: {e.caveat}" if e.caveat else ""
            lines.append(f"  - {e.claim}: {e.value} ({e.kind}; scorer {e.measured_by}; on {e.on_what};"
                         f" day {e.day}; files: {e.location or 'not recorded'}).{cav}")
        if not self.evidence:
            lines.append("  - nothing measured")
        lines += ["", "Blockers (named owner, days open):"]
        for r in blockers:
            lines.append(f"  - {r.key}: {r.what}; owner {_who(r.owner)}; open {_days(today - r.requested_day)}; "
                         f"blocks {r.blocks}")
        lines += ["", "Open findings:"]
        for n in findings:
            lines.append(f"  - day {n.day}, {n.author}: {n.text}")
        lines += ["", "Decisions needed (oldest first):"]
        for d in open_dec:
            due = f", due day {d.due_day}" if d.due_day is not None else ""
            lines.append(f"  - {d.key}: {d.question} Owner {_who(d.owner)}; open {_days(d.age(today))}{due}.")
        lines += ["", "Promises made to the customer, not yet verified:"]
        for n in promises:
            lines.append(f"  - day {n.day}, {n.author}: {n.text} (verifier: {n.verifier or 'none named'})")
        lines += ["", "Other requests in flight:"]
        for r in open_req:
            if not r.blocks:
                lines.append(f"  - {r.key}: {r.what}; owner {_who(r.owner)}; {r.status}")
        lines += ["", "Next week:"]
        for n in self.notes:
            if n.kind == "plan" and n.closed_day is None:
                lines.append(f"  - {n.text}")
        return "\n".join(lines) + "\n"

    # ---- files -----------------------------------------------------------------------------------
    _FOLDERS = {"notes": Note, "decisions": Decision, "access": Request, "evidence": Evidence}

    def save(self, root) -> pathlib.Path:
        root = pathlib.Path(root)
        for folder, items in (("notes", self.notes), ("decisions", self.decisions),
                              ("access", self.requests), ("evidence", self.evidence)):
            (root / folder).mkdir(parents=True, exist_ok=True)
            with open(root / folder / "records.jsonl", "w") as fh:
                for it in items:
                    fh.write(json.dumps(asdict(it), sort_keys=True) + "\n")
        (root / "status").mkdir(parents=True, exist_ok=True)
        (root / "ENGAGEMENT.md").write_text(f"# {self.customer}\n\nfieldkit engagement layer {LAYER}.\n")
        return root

    def write_status(self, root, today: int) -> pathlib.Path:
        p = pathlib.Path(root) / "status" / f"day{today:03d}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.status(today))
        return p

    @classmethod
    def load(cls, root) -> "EngagementRepo":
        root = pathlib.Path(root)
        customer = (root / "ENGAGEMENT.md").read_text().splitlines()[0].lstrip("# ").strip()
        repo = cls(customer)
        targets = {"notes": repo.notes, "decisions": repo.decisions, "access": repo.requests,
                   "evidence": repo.evidence}
        for folder, klass in cls._FOLDERS.items():
            f = root / folder / "records.jsonl"
            if f.exists():
                for line in f.read_text().splitlines():
                    if line.strip():
                        targets[folder].append(klass(**json.loads(line)))
        return repo
