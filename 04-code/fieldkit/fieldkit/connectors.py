"""fieldkit.connectors (book layer v2.4, Chapter 19): documents in and decisions out of systems with no API.

Six pieces, each small enough to read in one sitting:
  Surface / inventory_report   score every way in and out of a customer system, and list what is still unknown
  FileDrop                     a nightly export treated as an interface: arrival, header, volume, idempotency
  MailQueue                    a mailbox treated as a queue: durable write before acknowledge, two dedupe keys
  ScreenSpec / ScreenConnector a screen treated as a contract: fingerprint before every read or write
  Rule / WriteBack / Outbox    write-back with idempotency key, preflight against the production rule catalog,
                               postcondition read-back, compensation, and a human queue for everything held
  reconcile                    the integration test: expected against what the system of record now holds
  parse_x12 / edi_status       a small X12 reader with envelope checks, for carrier status messages
Pure standard library. Nothing here calls a model; the connectors are deterministic on purpose."""
from __future__ import annotations
import hashlib
import statistics
from dataclasses import dataclass, field

# ---------------------------------------------------------------- inventory
BASE = {"api": 1.00, "db_view": 0.85, "file_export": 0.75, "queue": 0.70, "mail": 0.60,
        "batch_loader": 0.55, "screen_robotic": 0.45, "screen_agent": 0.30}
FACTS = ("owner", "sample", "failure_contact", "change_notice")


@dataclass
class Surface:
    system: str
    name: str
    kind: str                    # a key of BASE
    direction: str               # "read" or "write"
    owner: str | None = None     # a named person who can change it
    sample: bool = False         # have we held a real sample of what crosses it
    failure_contact: str | None = None   # who hears about it when it breaks
    change_notice: str | None = None     # how changes to it are announced
    changes_per_year: int = 0

    def gaps(self):
        return [f for f in FACTS if not getattr(self, f)]

    def score(self):
        s = BASE[self.kind] - 0.08 * len(self.gaps()) - 0.03 * min(self.changes_per_year, 5)
        return round(max(s, 0.0), 2)


def inventory_report(surfaces):
    rows = sorted(surfaces, key=lambda s: (s.system, s.direction, -s.score()))
    return [(s.system, s.direction, s.name, s.kind, s.score(), ",".join(s.gaps()) or "-") for s in rows]


def best_path(surfaces, system, direction):
    c = [s for s in surfaces if s.system == system and s.direction == direction]
    return max(c, key=lambda s: s.score()) if c else None

# ---------------------------------------------------------------- file drop
@dataclass
class Batch:
    name: str
    status: str                  # accepted | duplicate | refused
    rows: int = 0
    reasons: list = field(default_factory=list)
    digest: str = ""


class FileDrop:
    """A nightly export is an interface whether or not anyone wrote it down. Check it like one."""

    def __init__(self, name, expected_header, deadline_min, low=0.6, high=1.5, window=20, key=None):
        self.name, self.expected, self.deadline = name, list(expected_header), deadline_min
        self.low, self.high, self.window, self.key = low, high, window, key
        self.seen: dict[str, str] = {}
        self.history: dict[str, list[int]] = {}

    def _band_key(self, label):
        return self.key(label) if self.key else "all"

    def check(self, filename, content: bytes, arrived_min, label=""):
        d = hashlib.sha256(content).hexdigest()[:16]
        if d in self.seen:
            return Batch(filename, "duplicate", 0, [f"same bytes as {self.seen[d]}"], d)
        reasons = []
        text = content.decode("utf-8", errors="replace").splitlines()
        if not text:
            return Batch(filename, "refused", 0, ["empty file"], d)
        header = [h.strip() for h in text[0].split(",")]
        if header != self.expected:
            added = [h for h in header if h not in self.expected]
            gone = [h for h in self.expected if h not in header]
            reasons.append(f"schema drift: added {added or '-'} removed {gone or '-'}")
        rows = len(text) - 1
        hist = self.history.setdefault(self._band_key(label), [])
        if len(hist) >= 5:
            med = statistics.median(hist[-self.window:])
            ratio = rows / med if med else 0
            if not (self.low <= ratio <= self.high):
                reasons.append(f"volume {rows} is {ratio:.2f} of trailing median {med:.0f}")
        if arrived_min > self.deadline:
            reasons.append(f"late: arrived {arrived_min // 60:02d}:{arrived_min % 60:02d}")
        hard = [r for r in reasons if not r.startswith("late")]
        if hard:
            return Batch(filename, "refused", rows, reasons, d)
        self.seen[d] = filename
        hist.append(rows)
        return Batch(filename, "accepted", rows, reasons, d)

    def missing(self, arrived: bool, now_min):
        return (not arrived) and now_min > self.deadline

# ---------------------------------------------------------------- mail queue
@dataclass
class Message:
    msg_id: str
    sender: str
    subject: str
    attachments: list            # list of (filename, bytes)


def attachment_key(m: Message):
    h = hashlib.sha256()
    for name, data in sorted(m.attachments):
        h.update(hashlib.sha256(data).digest())
    return h.hexdigest()[:16]


class MailQueue:
    """Read a mailbox as if it were a queue. Write durably first, acknowledge second, dedupe on two keys."""

    def __init__(self, keys=("msg_id", "attachments")):
        self.keys = keys
        self.store: dict[str, Message] = {}
        self.index: dict[str, str] = {}
        self.duplicates: list[tuple[str, str]] = []

    def accept(self, m: Message):
        ks = []
        if "msg_id" in self.keys:
            ks.append("id:" + m.msg_id)
        if "attachments" in self.keys and m.attachments:
            ks.append("att:" + attachment_key(m))
        for k in ks:
            if k in self.index:
                self.duplicates.append((m.msg_id, k.split(":")[0]))
                return False
        doc = f"doc-{len(self.store) + 1:04d}"
        self.store[doc] = m
        for k in ks:
            self.index[k] = doc
        return True

# ---------------------------------------------------------------- screens
class ScreenChanged(Exception):
    pass


def fingerprint(labels):
    return hashlib.sha256("|".join(labels).encode()).hexdigest()[:12]


@dataclass
class ScreenSpec:
    name: str
    labels: list                  # the visible labels, in order, that define this screen
    fields: dict                  # our field name -> the label it sits beside

    @property
    def fp(self):
        return fingerprint(self.labels)


class ScreenConnector:
    """Never type into a screen you have not recognized. Recognize it by its labels, not by coordinates."""

    def __init__(self, app, specs):
        self.app, self.specs = app, {s.name: s for s in specs}
        self.steps = 0

    def _check(self, name):
        spec, labels = self.specs[name], self.app.labels(name)
        if fingerprint(labels) != spec.fp:
            gone = [l for l in spec.labels if l not in labels]
            new = [l for l in labels if l not in spec.labels]
            raise ScreenChanged(f"{name}: fingerprint {fingerprint(labels)} != {spec.fp}; new {new} missing {gone}")
        return spec

    def read(self, name, key):
        spec = self._check(name); self.steps += 1
        raw = self.app.read(name, key)
        return {f: raw.get(lbl) for f, lbl in spec.fields.items()}

    def submit(self, name, values, key=None):
        spec = self._check(name); self.steps += 1
        return self.app.submit(name, {spec.fields.get(f, f): v for f, v in values.items()}, key)

# ---------------------------------------------------------------- write-back
@dataclass
class Rule:
    rule_id: str
    text: str
    check: object                 # callable(record) -> bool, True when the record passes


def preflight(record, rules):
    return [r.rule_id for r in rules if not r.check(record)]


@dataclass
class OutboxEntry:
    key: str
    record: dict
    state: str = "pending"        # pending | unknown | verified | held
    reasons: list = field(default_factory=list)
    target_id: str | None = None


class Outbox:
    def __init__(self):
        self.entries: dict[str, OutboxEntry] = {}

    def add(self, key, record):
        if key in self.entries:
            return self.entries[key], False
        self.entries[key] = OutboxEntry(key, dict(record))
        return self.entries[key], True

    def by_state(self):
        out = {}
        for e in self.entries.values():
            out[e.state] = out.get(e.state, 0) + 1
        return dict(sorted(out.items()))

    def held(self):
        return [e for e in self.entries.values() if e.state == "held"]


class WriteBack:
    """Write a decision into a system through its own front door, and prove it landed.

    target must offer: find(key) -> id|None, write(record, key) -> (ok, id|None, reason),
    readback(id) -> dict, void(id) -> bool. The key is stored in the target, so a retry finds it."""

    def __init__(self, target, rules=(), verify_fields=(), preflight_on=True, compensate=True):
        self.t, self.rules, self.vf = target, list(rules), list(verify_fields)
        self.preflight_on, self.compensate = preflight_on, compensate
        self.outbox = Outbox()

    def submit(self, key, record):
        e, new = self.outbox.add(key, record)
        if e.state in ("verified", "held", "compensated"):
            return e
        existing = self.t.find(key)
        if existing:                                   # a retry after an unknown outcome
            e.target_id = existing
            return self._verify(e)
        if self.preflight_on:
            failed = preflight(record, self.rules)
            if failed:
                e.state, e.reasons = "held", [f"preflight {r}" for r in failed]
                return e
        try:
            ok, tid, reason = self.t.write(record, key)
        except TimeoutError:                           # the write may or may not have landed
            e.state, e.reasons = "unknown", ["timeout after submit"]
            return e
        e.target_id = tid
        if not ok:
            if tid and self.compensate:
                self.t.void(tid)
                e.state, e.reasons = "held", [f"rejected {reason}; shell {tid} voided"]
            else:
                e.state, e.reasons = "held", [f"rejected {reason}" + (f"; shell {tid} left" if tid else "")]
            return e
        return self._verify(e)

    def _verify(self, e):
        got = self.t.readback(e.target_id)
        diffs = [f for f in self.vf if str(got.get(f)) != str(e.record.get(f))]
        if diffs:
            e.state, e.reasons = "held", [f"readback differs on {diffs}"]
        else:
            e.state = "verified"
        return e

# ---------------------------------------------------------------- reconciliation
@dataclass
class Recon:
    matched: list
    held: list
    missing: list
    extra: list
    mismatched: list

    def counts(self):
        return {k: len(getattr(self, k)) for k in ("matched", "held", "missing", "extra", "mismatched")}

    @property
    def unexplained(self):
        return len(self.missing) + len(self.extra) + len(self.mismatched)


def reconcile(expected: dict, actual: dict, fields, held=(), orphan=None):
    """expected: key -> record we meant to write; actual: key -> record the system of record holds (from its
    own export, never from our logs); held: keys a human queue owns; orphan(rec) marks a record that exists
    but should not (a shell a failed write left behind). Every expected key lands in exactly one bucket;
    extra lists records nobody expected, orphans included."""
    held, orphan = set(held), orphan or (lambda r: False)
    m, h, miss, extra, mm = [], [], [], [], []
    for k, rec in expected.items():
        got = actual.get(k)
        if got is not None and orphan(got):
            extra.append(k); got = None
        if k in held:
            h.append(k); continue
        if got is None:
            miss.append(k); continue
        diffs = [f for f in fields if str(got.get(f)) != str(rec.get(f))]
        if diffs:
            mm.append((k, diffs))
        else:
            m.append(k)
    extra += [k for k in actual if k not in expected]
    return Recon(m, h, miss, extra, mm)


# ---------------------------------------------------------------- EDI (X12)
class EDIError(Exception):
    pass


def parse_x12(text, seg="~", el="*"):
    """Split an interchange into transaction sets and check the envelope arithmetic a VAN will not check for you."""
    segs = [s.strip() for s in text.strip().split(seg) if s.strip()]
    if not segs or not segs[0].startswith("ISA"):
        raise EDIError("no ISA header")
    isa, iea = segs[0].split(el), segs[-1].split(el)
    if iea[0] != "IEA" or iea[2].strip() != isa[13].strip():
        raise EDIError("ISA/IEA control number mismatch")
    sets, cur, errors = [], None, []
    for s in segs[1:-1]:
        e = s.split(el)
        if e[0] == "ST":
            cur = {"st": e, "segs": [e]}
        elif e[0] == "SE" and cur is not None:
            cur["segs"].append(e)
            n = len(cur["segs"])
            if int(e[1]) != n:
                errors.append((cur["st"][2], f"SE01 says {e[1]} segments, counted {n}"))
            elif e[2] != cur["st"][2]:
                errors.append((cur["st"][2], "ST02/SE02 mismatch"))
            else:
                sets.append(cur["segs"])
            cur = None
        elif cur is not None:
            cur["segs"].append(e)
    return sets, errors


STATUS_214 = {"X3": "picked_up", "X1": "delivered", "AF": "departed", "X6": "en_route", "AG": "estimated",
              "D1": "delivered", "X4": "arrived", "SD": "delayed"}


def edi_status(tset):
    """One X12 214 transaction set -> (shipment, leg, status, stamp) or raises EDIError for an unknown code."""
    ref = next((e for e in tset if e[0] == "B10"), None)
    legv = next((e[1] for e in tset if e[0] == "L11" and len(e) > 2 and e[2] == "LG"), None)
    at7 = next((e for e in tset if e[0] == "AT7"), None)
    if not (ref and at7):
        raise EDIError("missing B10 or AT7")
    code = at7[1]
    if code not in STATUS_214:
        raise EDIError(f"unknown status code {code}")
    return ref[2], legv, STATUS_214[code], at7[5] + at7[6]
