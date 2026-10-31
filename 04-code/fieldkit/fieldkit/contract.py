"""fieldkit v4.2 (Chapter 34): procurement, legal and the contract.

A contract is read by engineering as a list of commitments. The extractor finds every sentence in which the vendor
promises something (shall, will, must, warrants, agrees to), sorts it by kind, and parses what a service level needs
to be computable: metric, unit, scorer, sample, window, threshold and remedy. The lint then asks four questions of
each commitment: can anyone measure it the same way twice (UNMEASURABLE, UNILATERAL MEASURE), does it depend on
something the vendor does not control (UNCONTROLLED INPUT), is there a cap (UNCAPPED), and does it contradict a
decision already signed (CONFLICT, AUTHORITY). Pricing turns each commitment into a cost line with a basis
(measured, estimated, assumed), and the margin functions report year-one gross margin beside two-year
renewal-weighted gross profit, as Chapter 2 requires.

Service levels for a probabilistic system are designed, not typed: `design_service_level` finds the smallest monthly
sample and breach rule such that a system running at the acceptable rate is rarely in breach (alpha) and a system at
the unacceptable rate is usually caught (power). Everything is exact binomial arithmetic; nothing calls a model.
"""
from dataclasses import dataclass, field
import math
import re

KINDS = ("service level", "data", "change", "notice", "audit", "staffing", "deliverable", "exit", "liability", "other")
PARTS = {
    "accuracy": ("metric", "unit", "scorer", "sample", "window", "threshold", "remedy"),
    "availability": ("metric", "measured_at", "window", "threshold", "remedy"),
    "response": ("metric", "deadline", "hours"),
}
OBLIGATION = re.compile(r"\b(Northlight|the Vendor|Vendor|Supplier)\b[^.]*?\b(shall|will|must|warrants|agrees to)\b")
CUSTOMER_OBLIGATION = re.compile(r"\b(shall|will|must)\b")
KIND_WORDS = (
    ("liability", r"indemnif|liab"),
    ("exit", r"transition assistance|after termination"),
    ("audit", r"\baudit"),
    ("change", r"change the underlying model|model version|change .*model|revalidat|substitute a model"),
    ("data", r"delete|process .*data|personal data|protected health|retain|bank data"),
    ("notice", r"\bnotify\b|\bnotice\b"),
    ("staffing", r"on site|engineers|on call"),
    ("deliverable", r"report|runbook|train|transfer knowledge|deliver|log events"),
    ("service level", r"accura|availab|respond|turnaround|matched|agreement rate|document error|material correction"),
)
NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "six": 6, "ten": 10, "twelve": 12}


@dataclass(frozen=True)
class Clause:
    cid: str
    text: str
    doc: str = ""


@dataclass
class Commitment:
    cid: str
    kind: str
    sentence: str
    metric: str = ""
    params: dict = field(default_factory=dict)
    remedy: str = ""
    findings: list = field(default_factory=list)

    @property
    def missing(self):
        need = PARTS.get(self.metric, ())
        have = dict(self.params, remedy=self.remedy, metric=self.metric)
        return [p for p in need if not have.get(p)]


def _sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.;])\s+", text) if s.strip()]


def _num(word):
    return NUMBER_WORDS.get(word.lower(), None) if not word.isdigit() else int(word)


def _parse(sentence):
    s = sentence
    p = {}
    if m := re.search(r"(\d+(?:\.\d+)?)%", s):
        p["threshold"] = float(m.group(1))
    if re.search(r"acceptance window", s):
        p["window"] = "acceptance window"
    elif re.search(r"each calendar month|per month|monthly|each month", s):
        p["window"] = "month"
    if m := re.search(r"as determined by (\w+)", s):
        p["determined_by"] = m.group(1)
    if m := re.search(r"scored by ([A-Z][\w']+(?: [A-Z][\w']+)*(?:'s [a-z]+)?)", s):
        p["scorer"] = m.group(1)
    if m := re.search(r"sample of (\d[\d,]*)", s):
        p["sample"] = int(m.group(1).replace(",", ""))
    if m := re.search(r"\b(post-review document error|per document|per field|per memo|per referral)\b", s):
        p["unit"] = m.group(1)
    if m := re.search(r"measured at (?:the )?([a-z' -]+?)(?:,| in | excluding|\.|$)", s):
        p["measured_at"] = m.group(1).strip()
    if m := re.search(r"excluding ([^.;]+)", s):
        p["excluding"] = m.group(1).strip()
    if m := re.search(r"within (\w+) (hour|hours|days|business days)", s):
        p["deadline"] = f"{_num(m.group(1))} {m.group(2)}"
    if re.search(r"24 hours a day|seven days a week", s):
        p["hours"] = "24x7"
    elif m := re.search(r"between (\d{1,2}:\d\d) and (\d{1,2}:\d\d)", s):
        p["hours"] = f"{m.group(1)}-{m.group(2)}"
    if re.search(r"without limit|unlimited", s):
        p["uncapped"] = True
    if m := re.search(r"capped at ([^.;]+)", s):
        p["cap"] = m.group(1).strip()
    return p


def _kind(sentence):
    low = sentence.lower()
    for k, pat in KIND_WORDS:
        if re.search(pat, low):
            return k
    return "other"


def _metric(sentence):
    low = sentence.lower()
    if re.search(r"accura|error|matched|agreement rate|material correction", low):
        return "accuracy"
    if "availab" in low:
        return "availability"
    if "respond" in low or "turnaround" in low:
        return "response"
    return ""


def extract(clauses):
    """Every vendor commitment in the clauses, in order. Credit sentences attach to the last service level."""
    out, customer, none = [], [], []
    for cl in clauses:
        n, last_sl, found = 0, None, False
        for s in _sentences(cl.text):
            if re.search(r"withhold acceptance", s) and last_sl is not None:
                last_sl.remedy = "acceptance withheld, re-test at vendor cost"
                found = True
                continue
            if re.search(r"\bcredit\b", s, re.I) and last_sl is not None:
                if m := re.search(r"credit (\d+)% of the monthly", s):
                    last_sl.remedy = f"credit {m.group(1)}% monthly fee"
                    last_sl.params["credit_pct"] = float(m.group(1))
                if m := re.search(r"capped at ([^.;]+)", s):
                    last_sl.params["credit_cap"] = m.group(1).strip()
                if re.search(r"each calendar month|per month|monthly|each month", s):
                    last_sl.params.setdefault("window", "month")
                found = True
                continue
            if OBLIGATION.search(s):
                n += 1; found = True
                k = _kind(s)
                c = Commitment(f"{cl.cid}.{n}", k, s, _metric(s) if k == "service level" else "", _parse(s))
                out.append(c)
                last_sl = c if k == "service level" else last_sl
            elif CUSTOMER_OBLIGATION.search(s):
                customer.append((cl.cid, s)); found = True
        if not found:
            none.append(cl.cid)
    return out, customer, none


@dataclass(frozen=True)
class Dependency:
    phrase: str        # words in a commitment that reveal the dependency
    owner: str         # who controls it
    note: str = ""


@dataclass(frozen=True)
class Decision:
    did: str
    phrase: str        # words in a commitment that contradict it
    text: str
    kind: str = "CONFLICT"   # or AUTHORITY (an action outside the signed release boundary)


def lint(commitments, vendor="Northlight", dependencies=(), decisions=(), naive=False):
    """Findings per commitment. naive=True is the v0 extractor: any number counts as a measure."""
    for c in commitments:
        f = []
        if c.kind == "service level" and not naive:
            if c.missing:
                f.append(("UNMEASURABLE", "missing " + ", ".join(c.missing)))
            if c.params.get("determined_by") and c.params["determined_by"] != vendor:
                f.append(("UNILATERAL MEASURE", f"as determined by {c.params['determined_by']}, no method"))
        low = c.sentence.lower()
        for d in dependencies:
            if d.phrase in low and not (c.params.get("excluding") and d.phrase.split()[0] in c.params["excluding"]):
                f.append(("UNCONTROLLED INPUT", f"{d.note or d.phrase} (controlled by {d.owner})"))
        if c.params.get("uncapped"):
            f.append(("UNCAPPED", "no limit on liability"))
        elif c.kind == "liability" and not c.params.get("cap"):
            f.append(("UNCAPPED", "no cap stated"))
        for d in decisions:
            if d.phrase in low:
                f.append((d.kind, f"{d.did}: {d.text}"))
        c.findings = f
    return commitments


def trigger_findings(customer_obligations):
    """Customer obligations that start money (acceptance, payment) must have a criterion someone can test."""
    out = []
    for cid, s in customer_obligations:
        if re.search(r"\baccept", s):
            if re.search(r"satisfaction|sole discretion|in its opinion", s):
                out.append((cid, "UNDEFINED TRIGGER", "acceptance at the customer's satisfaction"))
            elif not re.search(r"criteria|Exhibit", s):
                out.append((cid, "UNDEFINED TRIGGER", "acceptance with no criterion"))
            elif not re.search(r"business days after|deemed", s):
                out.append((cid, "NO DEEMED ACCEPTANCE", "silence never starts the clock"))
    return out


# ---- pricing and margin ------------------------------------------------------------------------------------

@dataclass(frozen=True)
class CostLine:
    key: str
    label: str
    amount: float
    basis: str          # measured, estimated, assumed


def year_one_margin(revenue, costs):
    rev = sum(revenue.values()); cost = sum(c.amount for c in costs)
    return (rev - cost) / rev, rev, cost


def renewal_weighted_two_year(gp1, gp2, renewal):
    return gp1 + renewal * gp2


# ---- service levels for a probabilistic system --------------------------------------------------------------

def binom_sf(k, n, p):
    """P(X >= k) for X ~ Binomial(n, p), exact, by summing the lower tail in log space."""
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    if p <= 0:
        return 0.0
    if p >= 1:
        return 1.0
    lp, lq = math.log(p), math.log1p(-p)
    lower = 0.0
    for i in range(k):
        lower += math.exp(math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * lp + (n - i) * lq)
    return max(0.0, 1.0 - lower)


def wilson_upper(k, n, z=1.96):
    if n == 0:
        return 1.0
    p = k / n; d = 1 + z * z / n
    return (p + z * z / (2 * n) + z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d


@dataclass(frozen=True)
class ServiceLevel:
    name: str
    metric: str
    scorer: str
    acceptable: float      # bad-event rate the contract calls normal
    unacceptable: float    # bad-event rate the customer must be told about
    n: int                 # monthly sample
    k: int                 # breach if bad events in the sample >= k

    def p_breach(self, rate):
        return binom_sf(self.k, self.n, rate)

    @property
    def threshold_pct(self):
        return 100.0 * self.k / self.n


def design_service_level(name, metric, scorer, acceptable, unacceptable, alpha=0.05, power=0.80,
                         n_min=20, n_max=3000, step=10):
    """Smallest monthly sample n (in steps) and breach count k with P(breach|acceptable) <= alpha and
    P(breach|unacceptable) >= power. Returns None when no n up to n_max works."""
    for n in range(n_min, n_max + 1, step):
        k = max(1, int(acceptable * n))
        while binom_sf(k, n, acceptable) > alpha:
            k += 1
        if binom_sf(k, n, unacceptable) >= power:
            return ServiceLevel(name, metric, scorer, acceptable, unacceptable, n, k)
    return None


def point_rule(name, metric, scorer, acceptable, unacceptable, n, threshold):
    """The rule most contracts are written with: breach when the observed rate exceeds the threshold."""
    k = math.floor(threshold * n) + 1
    return ServiceLevel(name, metric, scorer, acceptable, unacceptable, n, k)


def zero_tolerance_breach(per_item_miss, items_per_month):
    """Probability that a 'no misses, ever' clause is breached in a month."""
    return 1 - (1 - per_item_miss) ** items_per_month


def services_net(hours, rate, billing, fee=0.0, bill_rate=0.0, cap=None):
    """Vendor's services net for a given number of delivery hours under fixed price or T&M with an optional cap."""
    cost = hours * rate
    if billing == "fixed":
        return fee - cost
    revenue = hours * bill_rate
    if cap is not None:
        revenue = min(revenue, cap)
    return revenue - cost
