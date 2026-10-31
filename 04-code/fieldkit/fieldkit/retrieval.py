"""fieldkit v3 (Chapter 23): retrieval on the customer's documents, under the customer's controls and cost.

Passages inherit their access-control list (ACL) from the source record at ingest and refuse records with none
(fail closed). Permission and lifecycle filters run before ranking, never after. Supersession is explicit
metadata (state, superseded_by, superseded_on) set by the document owner, and the context header tells the model
when a passage stopped applying. Questions written by the customer's experts are scored with recall at k per
category. Cost lines are attributed to the party that pays and the cost center that is charged.
Pure Python, no vector database: the lab's embedding is a deterministic stand-in for the customer's gateway."""
from __future__ import annotations
import math, re
from collections import Counter, defaultdict
from dataclasses import dataclass, field

TOKEN = re.compile(r"[a-z0-9]+")
STATES = ("current", "superseded", "draft", "withdrawn")


def tokens(s: str) -> list[str]:
    return TOKEN.findall(s.lower())


@dataclass
class Passage:
    pid: str
    doc_id: str
    version: str
    section: str
    text: str
    acl: frozenset
    effective_from: int
    state: str = "current"
    superseded_by: str | None = None
    superseded_on: int | None = None
    owner: str = ""
    acl_synced: int = 0

    def valid_on(self, day: int | None) -> bool:
        """In force on `day` (None means today's current state only)."""
        if day is None:
            return self.state == "current"
        if self.state in ("draft", "withdrawn") or self.effective_from > day:
            return False
        return self.superseded_on is None or day < self.superseded_on


@dataclass(frozen=True)
class Principal:
    user: str
    groups: frozenset

    def can_read(self, p: Passage) -> bool:
        return bool(self.groups & p.acl)


@dataclass(frozen=True)
class Audience:
    """Several participants in one interaction: a passage is allowed only if every one of them may read it."""
    members: tuple

    @property
    def user(self):
        return "+".join(m.user for m in self.members)

    def can_read(self, p: Passage) -> bool:
        return all(m.can_read(p) for m in self.members)


class IngestRefused(Exception):
    pass


class Index:
    def __init__(self, embed=None, k1: float = 1.2, b: float = 0.75):
        self.passages: dict[str, Passage] = {}
        self.tf: dict[str, Counter] = {}
        self.df: Counter = Counter()
        self.vec: dict[str, dict] = {}
        self.embed = embed
        self.k1, self.b = k1, b
        self.refused: list[tuple[str, str]] = []
        self.embedded_tokens = 0
        self.post, self.vpost, self.vnorm = {}, {}, {}

    # ingest -------------------------------------------------------------------------------------------
    def ingest(self, records, day: int = 0):
        """records: dicts with pid, doc_id, version, section, text, acl (from the source) and lifecycle fields."""
        n = 0
        for r in records:
            if not r.get("acl"):
                self.refused.append((r["pid"], "no ACL on the source record"))
                continue
            p = Passage(r["pid"], r["doc_id"], r.get("version", "1"), r.get("section", ""), r["text"],
                        frozenset(r["acl"]), r.get("effective_from", 0), r.get("state", "current"),
                        r.get("superseded_by"), r.get("superseded_on"), r.get("owner", ""), day)
            if p.pid in self.passages:
                self.refused.append((p.pid, "duplicate passage id"))
                continue
            if p.state not in STATES:
                self.refused.append((p.pid, f"unknown state {p.state}"))
                continue
            t = Counter(tokens(p.text + " " + p.section))
            self.passages[p.pid], self.tf[p.pid] = p, t
            self.df.update(t.keys())
            for w in t:
                self.post.setdefault(w, set()).add(p.pid)
            if self.embed:
                v = self.embed(p.text + " " + p.section)
                self.vec[p.pid] = v; self.vnorm[p.pid] = math.sqrt(sum(x * x for x in v.values())) or 1.0
                for w in v:
                    self.vpost.setdefault(w, set()).add(p.pid)
                self.embedded_tokens += sum(t.values())
            n += 1
        self._avg = sum(sum(c.values()) for c in self.tf.values()) / max(1, len(self.tf))
        return n

    def sync_acl(self, source_acl: dict, day: int):
        """Copy the source's current ACL onto every passage of each document; return the documents that changed."""
        changed = []
        for p in self.passages.values():
            new = frozenset(source_acl.get(p.doc_id, p.acl))
            if new != p.acl:
                changed.append(p.doc_id)
                p.acl = new
            p.acl_synced = day
        return sorted(set(changed))

    def set_state(self, doc_id: str, state: str, superseded_by=None, on=None, by: str = ""):
        if state not in STATES:
            raise ValueError(state)
        if state == "superseded" and (not superseded_by or on is None):
            raise ValueError("a superseded document names its successor and the day it stopped applying")
        hit = 0
        for p in self.passages.values():
            if p.doc_id == doc_id:
                p.state, p.superseded_by, p.superseded_on = state, superseded_by, on
                if by:
                    p.owner = by
                hit += 1
        return hit

    # ranking ------------------------------------------------------------------------------------------
    def _bm25(self, q, pids):
        N = len(self.passages); out = defaultdict(float); pool = set(pids)
        for t in set(tokens(q)):
            if t not in self.post:
                continue
            idf = math.log(1 + (N - self.df[t] + 0.5) / (self.df[t] + 0.5))
            for pid in self.post[t] & pool:
                tf = self.tf[pid]; f = tf[t]; L = sum(tf.values())
                out[pid] += idf * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * L / self._avg))
        return dict(out)

    def _cos(self, q, pids):
        qv = self.embed(q); qn = math.sqrt(sum(v * v for v in qv.values())) or 1.0
        out = defaultdict(float); pool = set(pids)
        for w, x in qv.items():
            for pid in self.vpost.get(w, set()) & pool:
                out[pid] += x * self.vec[pid][w]
        return {pid: d / (qn * self.vnorm[pid]) for pid, d in out.items() if d > 0}

    def rank(self, query, pids, mode="hybrid", rrf_k=60, identifiers=True):
        """hybrid fuses lexical and vector ranks (reciprocal rank fusion). With identifiers=True a query that
        carries a code or form number (any token with a digit) weights the lexical side three times, because
        embeddings do not tell CF 04 90 from CF 04 09."""
        if mode == "lexical":
            s = self._bm25(query, pids)
        elif mode == "vector":
            s = self._cos(query, pids)
        else:
            s = defaultdict(float)
            wl = 3.0 if identifiers and any(ch.isdigit() for ch in query) else 1.0
            for wt, part in ((wl, self._bm25(query, pids)), (1.0, self._cos(query, pids))):
                for r, pid in enumerate(sorted(part, key=lambda x: (-part[x], x))):
                    s[pid] += wt / (rrf_k + r + 1)
        return sorted(s.items(), key=lambda kv: (-kv[1], kv[0]))

    def search(self, query, who, k=10, mode="hybrid", as_of=None, acl="pre", lifecycle=True, recency=0.0,
               identifiers=True):
        """acl: 'pre' filters before ranking (the rule), 'post' ranks everything then drops what `who` may not read,
        'none' ignores permissions (the failure). lifecycle=False ignores state and validity (the failure).
        recency > 0 boosts newer effective dates, which is the common half-fix."""
        pool = list(self.passages)
        if lifecycle:
            pool = [p for p in pool if self.passages[p].valid_on(as_of)]
        if acl == "pre":
            pool = [p for p in pool if who.can_read(self.passages[p])]
        ranked = self.rank(query, pool, mode, identifiers=identifiers)
        if recency:
            eff = [self.passages[p].effective_from for p in pool] or [0]
            lo, span = min(eff), (max(eff) - min(eff)) or 1
            ranked = sorted(((p, s * (1 + recency * (self.passages[p].effective_from - lo) / span)) for p, s in ranked),
                            key=lambda kv: (-kv[1], kv[0]))
        hits = ranked[:k]
        if acl == "post":
            hits = [(p, s) for p, s in hits if who.can_read(self.passages[p])]
        return [(self.passages[p], s) for p, s in hits]


def _date(x: int) -> str:
    s = str(x)
    return f"{s[:4]}-{s[4:6]}-{s[6:]}" if len(s) == 8 else f"day {s}"


def context_header(p: Passage, today: int) -> str:
    """The line the model sees above a passage. Supersession is stated, not left to a date."""
    h = f"[{p.doc_id} · {p.section} · effective {_date(p.effective_from)}]"
    if p.superseded_on is not None and p.superseded_on <= today:
        h += f" SUPERSEDED by {p.superseded_by} on {_date(p.superseded_on)}; do not apply to work after that date."
    elif p.state == "draft":
        h += " DRAFT, not approved; do not apply."
    return h


def acl_drift(index: Index, source_acl: dict):
    """Documents whose index ACL differs from the source; 'broader' ones are exposures."""
    out = []
    for doc, acl in sorted(source_acl.items()):
        ps = [p for p in index.passages.values() if p.doc_id == doc]
        if ps and ps[0].acl != frozenset(acl):
            out.append((doc, "broader" if not ps[0].acl <= frozenset(acl) else "narrower"))
    return out


# evaluation -------------------------------------------------------------------------------------------
@dataclass
class Question:
    qid: str
    text: str
    category: str
    gold: tuple = ()            # pids; empty means the answer is not in the documents
    as_of: int | None = None
    asked_by: str = ""


def evaluate(index: Index, questions, who, k=10, **kw):
    """Recall at k per question (share of gold passages in the top k), averaged over answerable questions,
    overall and by category, plus mean reciprocal rank of the first gold hit. `who` is a principal or a function of the question (its asker)."""
    per, cats, rr = {}, defaultdict(list), []
    for q in questions:
        if not q.gold:
            continue
        w = who(q) if callable(who) else who
        hits = [p.pid for p, _ in index.search(q.text, w, k=k, as_of=q.as_of, **kw)]
        r = sum(g in hits for g in q.gold) / len(q.gold)
        per[q.qid] = r; cats[q.category].append(r)
        first = next((i + 1 for i, h in enumerate(hits) if h in q.gold), None)
        rr.append(1.0 / first if first else 0.0)
    n = len(per)
    return dict(n=n, recall=sum(per.values()) / max(1, n), mrr=sum(rr) / max(1, n),
                by_category={c: (len(v), sum(v) / len(v)) for c, v in sorted(cats.items())}, per=per)


# cost -------------------------------------------------------------------------------------------------
@dataclass
class CostLine:
    item: str
    payer: str
    cost_center: str
    kind: str          # one-time | monthly | per-event
    usd: float
    basis: str = ""


@dataclass
class CostMeter:
    lines: list = field(default_factory=list)

    def add(self, *a, **kw):
        self.lines.append(CostLine(*a, **kw)); return self.lines[-1]

    def unattributed(self):
        return [l for l in self.lines if not l.payer or not l.cost_center]

    def monthly_by_payer(self):
        out = defaultdict(float)
        for l in self.lines:
            if l.kind == "monthly":
                out[l.payer] += l.usd
        return dict(out)

    def total(self, kind):
        return sum(l.usd for l in self.lines if l.kind == kind)


def token_cost(n_tokens: float, usd_per_million: float) -> float:
    return n_tokens * usd_per_million / 1e6
