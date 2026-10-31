"""Caldwell Mutual discovery, days 8 to 26: the notes the FDE kept, as data (deterministic stand-in).

Everything here is a labeled stand-in built for the book: the paths, volumes and timings are invented to be
consistent with the running project, and the shadowed documents are generated from the path parameters with
fixed seeds, so every number in the chapter re-runs to the same value. No customer data is held: shadowed
documents are recorded as desk tokens (D12-07) with timings, never with names or numbers from the page.
"""
from __future__ import annotations

import random
import statistics
from dataclasses import dataclass

from discovery import DiscoveryLog, Note, QUESTIONS


@dataclass(frozen=True)
class PathSpec:
    pid: str
    name: str
    documented: bool
    volume: int          # documents a month, from the system report that counts them
    work_min: float      # median hands-on minutes, document on the happy path
    exc_min: float       # median hands-on minutes, document that leaves the happy path
    lag_days: float      # mean days from arrival to a claim record
    exc_rate: float      # share of documents that leave the happy path
    exc_mix: tuple       # weights over EXCEPTIONS


EXCEPTIONS = ("existing claim, not new", "policy number missing or unreadable", "duplicate via a second door",
              "wrong line of business", "loss date missing", "several claims in one envelope", "not a claim")

PATHS = [
    PathSpec("P01", "paper mail, Hartford mailroom", True, 4100, 6.5, 19, 1.4, 0.24, (3, 3, 1, 1, 2, 2, 2)),
    PathSpec("P02", "main claims fax line", True, 2300, 5.0, 16, 0.1, 0.20, (3, 4, 2, 1, 2, 0, 1)),
    PathSpec("P03", "claims shared mailbox", True, 2900, 4.5, 14, 0.6, 0.27, (4, 2, 4, 1, 2, 0, 2)),
    PathSpec("P04", "agent portal upload", False, 2450, 3.5, 12, 0.4, 0.30, (5, 1, 4, 2, 1, 0, 0)),
    PathSpec("P05", "closed Springfield fax number, forwarded", False, 610, 7.0, 21, 2.1, 0.45, (2, 6, 2, 1, 1, 0, 1)),
    PathSpec("P06", "email to an adjuster, forwarded", False, 540, 6.0, 18, 3.2, 0.52, (6, 1, 4, 1, 1, 0, 0)),
    PathSpec("P07", "phone report, papers follow by mail", False, 980, 8.5, 24, 1.1, 0.62, (8, 2, 2, 0, 1, 0, 0)),
    PathSpec("P08", "administrator's nightly file transfer", False, 420, 2.5, 15, 0.9, 0.14, (2, 1, 3, 3, 1, 0, 0)),
    PathSpec("P09", "mail routed through the finance cage", False, 160, 9.0, 26, 4.8, 0.70, (5, 2, 1, 1, 1, 1, 2)),
    PathSpec("P10", "attorney letters through legal", False, 230, 11.0, 31, 5.5, 0.83, (7, 2, 1, 0, 1, 1, 0)),
    PathSpec("P11", "repair-estimate platform email", False, 110, 3.0, 10, 0.7, 0.35, (5, 1, 2, 0, 1, 0, 1)),
]
SPEC = {p.pid: p for p in PATHS}
NAMES = {p.pid: p.name for p in PATHS}
DOCUMENTED = [p.pid for p in PATHS if p.documented]
INTAKE_COST_PER_HOUR = 46.0   # Caldwell's loaded intake cost, from Anne Kessler's budget (stand-in)

# (day, who was shadowed, where, {path: documents watched}, questions answered for paths limited to some)
SESSIONS = [
    (12, "Tom Whitfield", "intake desk, mailroom cover", {"P01": 26, "P05": 7, "P04": 5, "P02": 3}),
    (14, "intake clerk A", "shared mailbox queue", {"P03": 22, "P02": 6, "P07": 9, "P06": 4}),
    (18, "intake clerk B", "Monday mail backlog", {"P01": 30, "P04": 8, "P08": 6}),
    (19, "Tom Whitfield", "intake desk, mailroom cover", {"P01": 18, "P05": 6, "P02": 4, "P06": 3, "P09": 2}),
    (21, "legal mail coordinator", "legal department", {"P10": 7, "P04": 12}),
    (22, "adjuster team lead", "adjuster inboxes", {"P06": 6, "P07": 8, "P03": 10}),
]
PARTIAL = {"P09": ("arrive", "touch")}   # two documents at the finance cage: seen arriving and moving, nothing more


@dataclass
class Watched:
    token: str
    day: int
    path: str
    work_min: float
    lag_days: float
    exception: str | None
    touches: int


def watched_documents(upto=None):
    docs = []
    for day, who, where, counts in SESSIONS:
        if upto is not None and day > upto:
            continue
        k = 0
        for pid, n in counts.items():
            p = SPEC[pid]
            rng = random.Random(f"caldwell-{day}-{pid}")
            for _ in range(n):
                k += 1
                exc = None
                if rng.random() < p.exc_rate:
                    exc = rng.choices(EXCEPTIONS, weights=p.exc_mix)[0]
                base = p.exc_min if exc else p.work_min
                work = round(base * rng.uniform(0.7, 1.35), 1)
                lag = max(0.0, round(p.lag_days * rng.uniform(0.6, 1.4) + (0.8 if exc else 0.0) * rng.random(), 1))
                touches = 2 + (2 if exc else 0) + (1 if not p.documented else 0) + rng.randint(0, 1)
                docs.append(Watched(f"D{day}-{k:02d}", day, pid, work, lag, exc, touches))
    return docs


def _shadow_notes():
    notes = []
    docs = watched_documents()
    for day, who, where, counts in SESSIONS:
        for pid in counts:
            ds = [d for d in docs if d.day == day and d.path == pid]
            n = len(ds)
            qs = PARTIAL.get(pid, tuple(QUESTIONS))
            for q in qs:
                text = {"arrive": f"{n} documents seen arriving at {where}",
                        "touch": f"median {statistics.median(d.touches for d in ds):g} touches per document",
                        "decide": "triage decision watched: new claim or existing, which line",
                        "except": f"{sum(1 for d in ds if d.exception)} of {n} left the happy path",
                        "land": "claim record created; received date set to the keying date"}[q]
                attr = dict(attribute="lag_days", value=round(statistics.mean(d.lag_days for d in ds), 2)) \
                    if q == "land" else {}
                notes.append(Note(day, "shadow", who, pid, q, text, n=n, ref=f"shadow-{day}", **attr))
    return notes


def _procedure_notes():
    ref = "2014 intake procedure, 40 pages"
    out = []
    for pid in DOCUMENTED:
        for q in QUESTIONS:
            attr = dict(attribute="lag_days", value=0.0) if q == "land" else {}
            out.append(Note(8, "procedure", "intake procedure (2014)", pid, q,
                            f"section for {NAMES[pid]}: {QUESTIONS[q].lower()}", ref=ref, **attr))
    return out


def _interviews():
    I = []
    for pid in DOCUMENTED:
        for q in QUESTIONS:
            attr = dict(attribute="lag_days", value=0.0) if q == "land" else {}
            I.append(Note(9, "interview", "Anne Kessler", pid, q, f"described {NAMES[pid]}", **attr))
    I += [Note(11, "interview", "mailroom lead", "P01", "arrive", "two scan batches named; only one runs"),
          Note(12, "interview", "Tom Whitfield", "P06", "arrive", "adjusters forward emails sent to them directly"),
          Note(12, "interview", "Tom Whitfield", "P07", "arrive", "papers that follow a phone report"),
          Note(16, "interview", "fax administrator", "P05", "touch", "closed office line forwarded since 2016"),
          Note(19, "interview", "Tom Whitfield", "P09", "arrive", "mail with a check goes to finance first"),
          Note(19, "interview", "Tom Whitfield", "P09", "decide", "finance decides whether it is a claim"),
          Note(20, "interview", "legal mail coordinator", "P10", "arrive", "letters of representation"),
          Note(25, "interview", "Anne Kessler", "P11", "arrive", "repair-estimate emails from the platform")]
    return I


def _artifacts():
    A = []
    rep = {"P01": (10, "mailroom log"), "P02": (10, "fax gateway report, main line"),
           "P03": (11, "shared mailbox report"), "P05": (13, "fax gateway report, legacy line"),
           "P04": (15, "agent portal export"), "P08": (16, "IT system inventory and transfer manifest"),
           "P07": (18, "call center report"), "P09": (20, "finance cage log"), "P10": (21, "legal mail log"),
           "P06": (22, "mailbox forwarding-rule count"), "P11": (23, "mailbox rules export")}
    for pid, (day, src) in rep.items():
        A.append(Note(day, "artifact", src, pid, "arrive", f"monthly count from {src}",
                      attribute="monthly_volume", value=float(SPEC[pid].volume)))
    for pid in ("P01", "P02", "P03", "P04", "P08"):
        A.append(Note(23, "artifact", "claims system received-date report", pid, "land",
                      "received date equals keying date on every record"))
    A.append(Note(23, "artifact", "mailbox rules export", "P11", "touch", "rule forwards to the shared mailbox"))
    return A


# Who gave the lead that found each undocumented path (the FDE's provenance column).
LEAD = {"P04": "Tom Whitfield", "P05": "Tom Whitfield", "P06": "Tom Whitfield", "P07": "Tom Whitfield",
        "P09": "Tom Whitfield", "P08": "IT system inventory", "P10": "legal mail coordinator",
        "P11": "mailbox rules export"}

# Tracer documents: synthetic first-notice forms, marked TEST, sent through a door with Anne Kessler's consent.
TRACERS = [(13, "P05"), (15, "P02"), (15, "P03")]


def _tracer_notes():
    out = []
    for day, pid in TRACERS:
        for q in QUESTIONS:
            attr = dict(attribute="lag_days", value=round(SPEC[pid].lag_days + (0.1 if pid == "P05" else 0.0), 2)) \
                if q == "land" else {}
            out.append(Note(day, "tracer", f"tracer {pid}", pid, q, f"tracer form timed through {NAMES[pid]}",
                            n=1, ref=f"tracer-{pid}", **attr))
    return out


def build_log(shadow=True, tracers=True, resolve=True):
    log = DiscoveryLog("Caldwell Mutual", NAMES, DOCUMENTED)
    log.add(*_procedure_notes(), *_interviews(), *_artifacts())
    if shadow:
        log.add(*_shadow_notes())
    if tracers:
        log.add(*_tracer_notes())
    if resolve:
        log.resolve("P01", "lag_days", "Anne Kessler", 14,
                    "procedure assumes two scan batches; the afternoon batch stopped in 2019")
        log.resolve("P03", "lag_days", "Anne Kessler", 15,
                    "mailbox is worked mornings only; observed lag accepted")
    return log
