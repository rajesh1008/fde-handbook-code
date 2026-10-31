"""fieldkit v3.6 (Chapter 29): the pyramid runner.

Five layers (unit, component, integration, system, operational), each with a coverage target, a frequency and a
cost per run. A change is classified by the paths it touches and only the layers that change can break are run
(change-aware selection). Every check returns one of three verdicts: pass, fail or inconclusive. The merge gate
blocks on any metric regression beyond its tolerance, on the aggregate and on every slice (document class, field,
question type), and holds an inconclusive slice until it has more data or an item-by-item sign-off in the change
ticket. There is no override flag.

Also here: control failures (seeded mutants the pyramid must catch at the layer designed to catch them), the
independence of verification streams (unique catches and correlation of misses), and test evidence records chained
by hash so a quality or model-risk reviewer can trace requirement to check to run to result.
"""
from dataclasses import dataclass, field, asdict
import hashlib
import json
import math

PASS, FAIL, INCONCLUSIVE, SKIPPED = "pass", "fail", "inconclusive", "skipped"
LAYER_NAMES = {1: "unit", 2: "component", 3: "integration", 4: "system", 5: "operational"}


@dataclass(frozen=True)
class Layer:
    n: int
    name: str
    coverage_target: str
    frequency: str
    seconds_budget: float
    dollars_budget: float


@dataclass
class Result:
    check: str
    layer: int
    verdict: str
    detail: str = ""
    seconds: float = 0.0
    dollars: float = 0.0
    metrics: dict = field(default_factory=dict)


# which layers a kind of change can break (Chapter 29, Table 29.2)
CHANGE_LAYERS = {"code": (1, 3), "rule": (1, 2, 3), "prompt": (1, 2, 3), "model": (1, 2, 3, 4),
                 "retrieval": (1, 2, 3), "threshold": (1, 2), "dependency": (1, 3), "gold": (2,),
                 "infra": (1, 3), "docs": ()}


def classify_path(path, rules):
    """rules: ordered [(prefix, kind)]. First prefix that matches wins; anything unmatched is 'code' (fail safe:
    an unknown path runs the code layers, never nothing)."""
    for prefix, kind in rules:
        if path.startswith(prefix):
            return kind
    return "code"


def select_layers(paths, rules, release=False):
    kinds = sorted({classify_path(p, rules) for p in paths})
    layers = set()
    for k in kinds:
        layers.update(CHANGE_LAYERS[k])
    if release:
        layers.update((1, 2, 3, 4))
    return kinds, sorted(layers)


def binom_tail(k, n, p=0.5):
    """P(X >= k) for X ~ Binomial(n, p)."""
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def paired_slices(before, after, slice_of):
    """before/after: {key: bool} on the same keys. Returns {slice: dict(n, before, after, gains, losses)}."""
    if set(before) != set(after):
        raise ValueError("before and after must be scored on the same items")
    out = {}
    for k in before:
        s = out.setdefault(slice_of(k), dict(n=0, before=0, after=0, gains=0, losses=0))
        b, a = before[k], after[k]
        s["n"] += 1; s["before"] += b; s["after"] += a
        s["gains"] += (a and not b); s["losses"] += (b and not a)
    return out


def slice_verdict(n, gains, losses, margin=0.02, alpha=0.05, min_n=30):
    """Paired sign test on the items that changed. Fail: the slice got worse and chance is an unlikely
    explanation. Inconclusive: worse by more than the margin but too few items or changes to tell."""
    if losses <= gains:
        return PASS, 1.0
    p = binom_tail(losses, gains + losses)
    drop = (losses - gains) / max(1, n)
    if p < alpha:
        return FAIL, p
    if drop > margin or n < min_n:
        return INCONCLUSIVE, p
    return PASS, p


@dataclass
class Metric:
    name: str
    before: float
    after: float
    higher_is_better: bool = True
    tolerance: float = 0.0

    @property
    def regression(self):
        return (self.before - self.after) if self.higher_is_better else (self.after - self.before)

    def verdict(self):
        return FAIL if self.regression > self.tolerance + 1e-12 else PASS


class MergeGate:
    """Blocks on any failed check; holds on an inconclusive check unless its id is signed off in the change
    ticket. A failed check cannot be signed off: the change goes back to its author."""

    def __init__(self, owner, ticket_signoffs=()):
        self.owner = owner
        self.signoffs = set(ticket_signoffs)

    def decide(self, results):
        fails = [r for r in results if r.verdict == FAIL]
        holds = [r for r in results if r.verdict == INCONCLUSIVE and r.check not in self.signoffs]
        if fails:
            first = min(r.layer for r in fails)
            return dict(decision="block", caught_at=first, reasons=[f"L{r.layer} {r.check}: {r.detail}" for r in fails])
        if holds:
            return dict(decision="hold", caught_at=min(r.layer for r in holds),
                        reasons=[f"L{r.layer} {r.check}: {r.detail} (needs {self.owner} or more data)" for r in holds])
        return dict(decision="merge", caught_at=None, reasons=[])


class Pyramid:
    def __init__(self, layers):
        self.layers = {l.n: l for l in layers}
        self.checks = {l.n: [] for l in layers}

    def add(self, layer, name, fn):
        """fn(system) -> Result fields as (verdict, detail, seconds, dollars, metrics)."""
        self.checks[layer].append((name, fn))
        return self

    def run(self, system, layers=None, stop_on_fail=True):
        out, stopped = [], False
        for n in sorted(layers or self.layers):
            for name, fn in self.checks[n]:
                if stopped:
                    out.append(Result(name, n, SKIPPED, "earlier layer failed"))
                    continue
                v, detail, sec, usd, metrics = fn(system)
                out.append(Result(name, n, v, detail, sec, usd, metrics))
            if stop_on_fail and any(r.layer == n and r.verdict == FAIL for r in out):
                stopped = True
        return out


def caught_at(results):
    bad = [r.layer for r in results if r.verdict in (FAIL, INCONCLUSIVE)]
    return min(bad) if bad else None


def totals(results):
    by = {}
    for r in results:
        t = by.setdefault(r.layer, dict(checks=0, seconds=0.0, dollars=0.0, verdicts={}))
        t["checks"] += 1; t["seconds"] += r.seconds; t["dollars"] += r.dollars
        t["verdicts"][r.verdict] = t["verdicts"].get(r.verdict, 0) + 1
    return by


@dataclass(frozen=True)
class Mutant:
    id: str
    what: str
    designed_layer: int
    apply: object   # callable(system) -> mutated system


def control_run(pyramid, base_system, mutants):
    """Run every seeded mutant through every layer (no early stop). A mutant caught after its designed layer is a
    late catch; one no layer catches is an escape. Either is a finding about the pyramid, not the agent."""
    rows = []
    for m in mutants:
        res = pyramid.run(m.apply(base_system), stop_on_fail=False)
        at = caught_at(res)
        status = "escaped" if at is None else ("caught" if at <= m.designed_layer else "late")
        rows.append(dict(id=m.id, what=m.what, designed=m.designed_layer, caught_at=at, status=status,
                         by=[r.check for r in res if r.verdict in (FAIL, INCONCLUSIVE)]))
    return rows


def independence(catches, defects):
    """catches: {stream: set(defect ids)}; defects: iterable of ids. Per stream: caught, unique (no other stream
    caught it); union; missed by all; and the phi correlation of misses for every pair."""
    defects = list(defects); D = len(defects)
    streams = list(catches)
    rows = {}
    for s in streams:
        others = set().union(*(catches[o] for o in streams if o != s)) if len(streams) > 1 else set()
        rows[s] = dict(caught=len(catches[s]), unique=len(catches[s] - others))
    union = set().union(*catches.values())
    phi = {}
    for i, a in enumerate(streams):
        for b in streams[i + 1:]:
            ma = [d not in catches[a] for d in defects]; mb = [d not in catches[b] for d in defects]
            n11 = sum(x and y for x, y in zip(ma, mb)); n10 = sum(x and not y for x, y in zip(ma, mb))
            n01 = sum(y and not x for x, y in zip(ma, mb)); n00 = D - n11 - n10 - n01
            den = math.sqrt(max(1e-12, (n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00)))
            phi[(a, b)] = (n11 * n00 - n10 * n01) / den
    return dict(rows=rows, union=len(union), missed=D - len(union), n=D, phi=phi)


@dataclass
class EvidenceRecord:
    requirement: str
    check: str
    layer: int
    run_id: str
    commit: str
    verdict: str
    metrics: dict
    prev: str = ""

    def digest(self):
        body = json.dumps({k: v for k, v in asdict(self).items()}, sort_keys=True)
        return hashlib.sha256(body.encode()).hexdigest()


def chain(records):
    prev = ""
    for r in records:
        r.prev = prev
        prev = r.digest()
    return prev


def verify(records):
    """Returns the index of the first record whose link is broken, or None."""
    prev = ""
    for i, r in enumerate(records):
        if r.prev != prev:
            return i
        prev = r.digest()
    return None


def trace_matrix(requirements, records):
    """requirements: {id: text}. Returns {id: dict(checks, last, covered)}; a requirement with no check that ran is
    uncovered and cannot be offered as gate evidence."""
    out = {rid: dict(checks=set(), last=None, covered=False) for rid in requirements}
    for r in records:
        if r.requirement in out:
            o = out[r.requirement]
            o["checks"].add(r.check); o["last"] = r.verdict; o["covered"] = True
    return out
