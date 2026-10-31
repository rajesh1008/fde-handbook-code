"""The whole Caldwell intake agent as one pipeline (Chapter 31 lab, deterministic stand-in).

Real fieldkit pieces: autonomy (the Signature 3 tree), routing (evidence gates, route_field, route_document),
guardrails (rule cards and the suite) and pyramid (layers and the merge gate). Stand-ins: OCR, the C06 and C07
small models, the C11 extractor, retrieval and the gateway transport, each returning hash-drawn outputs with the
same shape the earlier chapters' labs return. Nothing here is Caldwell data."""
from dataclasses import dataclass, field
import _paths  # noqa: F401
from fieldkit.autonomy import Step
from fieldkit.routing import Thresholds, Evidence, route_field, route_document
from fieldkit.guardrails import RuleCard, GuardrailSuite
from fieldkit.pyramid import Layer, Pyramid, PASS, FAIL
from world import u, FIELDS, CRITICAL, RELEASE
from state import Value, scope_check, ScopeViolation

TH = Thresholds(proceed=0.95, floor=0.47, target=0.98, lower_bound=0.0, checked_n=0)  # Ch27 v1.1; bound in Ch27

STEPS = [
    Step("C01", "capture text (OCR for fax, mail and portal pages)", determined=True),
    Step("C02", "date received from stamp or fax header", determined=True),
    Step("C03", "policy number pattern and check digit", determined=True),
    Step("C04", "coverage lookup in claims-core", determined=True),
    Step("C05", "match to an existing claim", determined=True),
    Step("C06", "document type: four signed types or none", closed_output=True, check="type in closed set; 0.90 or a person"),
    Step("C07", "loss cause code from the narrative", closed_output=True, check="code in loss-code table; 0.85 or a person"),
    Step("C08", "fixed zones on Caldwell and agency forms", determined=True),
    Step("C09", "fast-track and adjuster routing", written_rules=True, rule_owner="Anne Kessler"),
    Step("C10", "special-investigation indicators", written_rules=True, rule_owner="SIU lead"),
    Step("C11", "cited first-notice summary and free-text fields"),
    Step("C12", "write the claim record and queue item", determined=True),
]
WHERE = {"C01": "OCR service, Caldwell AWS", "C02": "intake service, Caldwell AWS", "C03": "intake service, Caldwell AWS",
         "C04": "claims-core read, svc-nl-claims-ro", "C05": "claims-core read, svc-nl-claims-ro",
         "C06": "gateway -> c06-p4", "C07": "gateway -> c07-small-2", "C08": "intake service, Caldwell AWS",
         "C09": "rules service, manual CM", "C10": "rules service, manual CM",
         "C11": "gateway -> extract-2026-04 + index", "C12": "proposal -> authorizer"}

CARDS = [
    RuleCard("CW-I-01", "no model step runs on a page with legibility under 0.50", "input", "engineering",
             "Anne Kessler", "Ruth Calloway", 150, effect="route", route_to="intake clerk", since="v1.1"),
    RuleCard("CW-I-02", "instructions inside a document are data, never commands", "input", "redteam",
             "Priya Natarajan", "Priya Natarajan", 128, effect="flag"),
    RuleCard("CW-O-01", "a water loss carries a cause code (V-118)", "output", "signed", "Joan Mercer",
             "Joan Mercer", 132, effect="route", route_to="adjuster", modality="oblige"),
    RuleCard("CW-O-02", "a claimant name over 30 characters is never cut silently", "output", "engineering",
             "Priya Natarajan", "Tom Whitfield", 104, effect="route", route_to="intake clerk"),
    RuleCard("CW-O-03", "every draft value was read from this claim's documents", "output", "boundary",
             "Anne Kessler", "Anne Kessler", 154, effect="block", route_to="intake clerk"),
    RuleCard("CW-A-01", "only create_intake_draft and attach_document (release boundary v2)", "action",
             "boundary", "Anne Kessler", "Daniel Reyes", 118, effect="block"),
    RuleCard("CW-B-01", "at most 3 model calls per document", "budget", "engineering", "Priya Natarajan",
             "Priya Natarajan", 120, effect="route", route_to="intake clerk"),
    RuleCard("CW-B-02", "at most $0.10 of model spend per document", "budget", "engineering", "Daniel Reyes",
             "Daniel Reyes", 120, effect="route", route_to="intake clerk"),
]
ALLOWED = {"create_intake_draft", "attach_document"}
CHECKS = {
    "CW-I-01": lambda c: (c["legibility"] >= 0.50, f"legibility {c['legibility']:.2f}"),
    "CW-I-02": lambda c: ("ignore previous" not in c.get("text", "").lower(), "instruction-like text"),
    "CW-O-01": lambda c: (c["values"]["loss_type"].value != "water" or "cause_code" in c["values"], "V-118"),
    "CW-O-02": lambda c: (len(str(c["values"]["claimant_name"].value)) <= 30, "claimant over 30 characters"),
    "CW-O-03": lambda c: (not scope_check(c["key"], c["values"]), f"foreign values {scope_check(c['key'], c['values'])}"),
    "CW-A-01": lambda c: (c["op"] in ALLOWED, f"operation {c['op']}"),
    "CW-B-01": lambda c: (c["calls"] <= 3, f"{c['calls']} calls"),
    "CW-B-02": lambda c: (c["dollars"] <= 0.10, f"${c['dollars']:.4f}"),
}
SUITE = GuardrailSuite(CARDS, CHECKS, version="cw-rules v1")


class Gateway:
    """Stand-in transport behind the fieldkit v2.3 adapter: records calls per app identity and pin."""
    PRICE = {"c06-p4": 0.011175, "c06-ft1": 0.00027, "c07-small-2": 0.00030}
    RATE_IN, RATE_OUT = 3.00 / 1e6, 15.00 / 1e6       # stand-in rate card, dollars per token

    def __init__(self, identity="nl-shadow", pin=RELEASE["pin"]):
        self.identity, self.pin, self.calls = identity, pin, []

    def call(self, model, doc_id, tin=0, tout=0):
        usd = self.PRICE.get(model, tin * self.RATE_IN + tout * self.RATE_OUT)
        self.calls.append((model, doc_id, tin, tout, usd))
        return usd


@dataclass
class Doc:
    id: str
    day: int
    channel: str
    kind: str                       # T1, T2, T3, T4 or none
    key: str                        # intake key, the value claims-core keeps in Agent Ref
    truth: dict = field(default_factory=dict)
    rotated: int = 0
    narrative: bool = True
    text: str = ""


@dataclass
class Release:
    orientation: bool = True        # C01 tries four angles and keeps the most legible
    legibility_gate: bool = True    # CW-I-01 enforced before C06
    examples_from_other_claims: bool = False   # Try It 2: the cross-claim memory the boundary refuses
    mode: str = "shadow"


def run(doc, rel, gw, store=None, example=None):
    """One document through C01 to C12. Returns (trace lines, outcome dict)."""
    tr, calls, usd = [], 0, 0.0
    native = doc.channel == "email"
    leg = 0.99 if native else round(0.86 + 0.12 * u("leg", doc.id), 2)
    note = "native text" if native else f"{1 + int(3 * u('pages', doc.id))} pages OCR"
    if doc.rotated:
        if rel.orientation:
            leg = round(0.40 + 0.55 * u("leg-fixed", doc.id), 2)
            note += f", rotated {doc.rotated}, corrected"
        else:
            leg = round(0.08 + 0.12 * u("leg-rot", doc.id), 2)
            note += f", rotated {doc.rotated}, not detected"
    tr.append(("C01", "det", WHERE["C01"], f"{note}, legibility {leg:.2f}"))
    din = SUITE.run("input", dict(legibility=leg, text=doc.text))
    if din.effect == "route" and rel.legibility_gate:
        tr.append(("gate", "rule", "CW-I-01", f"{din.failed[0].reason}: to {din.route_to}, no model call"))
        return tr, dict(band="escalate", reason="illegible", kind=None, calls=0, dollars=0.0)
    if leg < 0.50:
        kind, conf = "none", round(0.95 + 0.04 * u("conf-none", doc.id), 2)    # confident about garbage
    else:
        kind, conf = doc.kind, round(0.93 + 0.06 * u("conf", doc.id), 2)
    usd += gw.call(RELEASE["c06"], doc.id); calls += 1
    tr.append(("C06", "small", WHERE["C06"], f"type {kind}, confidence {conf:.2f}"))
    if kind == "none":
        tr.append(("exit", "-", "correspondence queue", "out of scope: no intake record, no routing"))
        return tr, dict(band="none: correspondence queue", reason="typed none", kind=kind, calls=calls, dollars=usd)
    k = doc.key
    vals = {f: Value(doc.truth.get(f, ""), k, f"{doc.id} p1") for f in FIELDS}
    tr.append(("C02", "det", WHERE["C02"], f"date received {doc.truth['date_received']}"))
    tr.append(("C03", "det", WHERE["C03"], f"policy {doc.truth['policy_number']}, check digit ok"))
    tr.append(("C04", "det", WHERE["C04"], "coverage in force on loss date"))
    tr.append(("C05", "det", WHERE["C05"], "no open claim on this policy and loss date: new intake"))
    if doc.narrative:
        usd += gw.call(RELEASE["c07"], doc.id); calls += 1
        vals["cause_code"] = Value(doc.truth.get("cause_code", ""), k, f"{doc.id} p1 narrative")
        tr.append(("C07", "small", WHERE["C07"], f"cause code {doc.truth.get('cause_code', '')}"))
    tr.append(("C08", "det", WHERE["C08"], "no fixed zones (letter or email)" if doc.kind == "T3" else "form zones read"))
    tr.append(("C09", "rules", WHERE["C09"], "not fast-track: injury reported" if doc.truth.get("injury_reported") == "yes"
               else "fast-track eligible"))
    tr.append(("C10", "rules", WHERE["C10"], "0 indicators"))
    passages = ["CM-WL-07 v3 s4.2", "CM-WL-07 v3 s4.5"] if doc.truth.get("loss_type") == "water" else ["CM-GN-01 s2.1"]
    usd += gw.call(RELEASE["pin"], doc.id, 5200, 450); calls += 1
    if example is not None and rel.examples_from_other_claims:
        vals["other_party"] = example        # the copied detail from another claim's draft
    tr.append(("C11", "frontier", WHERE["C11"], f"10 fields + summary, 7 citations, passages {', '.join(passages)}"))
    routes = []
    for f in FIELDS:
        s = round(0.93 + 0.069 * u("score", doc.id, f), 3)
        ev = Evidence(found_in_source=True, system_check=True if f in ("policy_number", "loss_date") else None)
        routes.append(route_field(s, ev, TH))
    band, reason = route_document(routes, FIELDS, CRITICAL)
    low = [f"{f} {r.score:.2f}" for f, r in zip(FIELDS, routes) if r.band != "proceed"]
    tr.append(("router", "v1.1", "brain, Caldwell AWS", f"{10 - len(low)} proceed, {len(low)} review "
               f"({'; '.join(low) or 'none'}) -> {band}"))
    dout = SUITE.run("output", dict(values=vals, key=k))
    dact = SUITE.run("action", dict(op="create_intake_draft"))
    dbud = SUITE.run("budget", dict(calls=calls, dollars=usd))
    flagged = [f"{v.rid} {v.effect}" for d in (dout, dact, dbud) for v in d.failed]
    tr.append(("guards", "rules", SUITE.version, f"{len(SUITE.live())} cards, failed: {', '.join(flagged) or 'none'}"))
    if dout.effect == "block":
        tr.append(("C12", "det", WHERE["C12"], f"blocked by {dout.failed[0].rid}: {dout.failed[0].reason}"))
        return tr, dict(band="blocked", reason=dout.failed[0].rid, kind=kind, calls=calls, dollars=usd)
    tr.append(("C12", "det", WHERE["C12"], "propose create_intake_draft -> authorized (boundary v2) -> "
               + ("not executed: mode shadow" if rel.mode == "shadow" else "executed, verified")))
    if store is not None:
        store.open(k, rel.mode, doc.day)
        for name, v in vals.items():
            store.put(k, name, v, doc.day)
        store.put(k, "route", Value(band, k, "router v1.1"), doc.day)
    return tr, dict(band=band, reason=reason, kind=kind, calls=calls, dollars=usd)


def rotated_faxes(n=24, seed="slice"):
    kinds = ["T1", "T2", "T1", "T4"]
    return [Doc(f"R-{seed}-{i:02d}", 149, "fax", kinds[i % 4], f"IK-R{i:02d}", rotated=(90, 180, 270)[i % 3],
                truth=dict(date_received="day 149", policy_number="synthetic"), narrative=False)
            for i in range(n)]


def c06_slice(rel):
    gw, typed_none, right, escal = Gateway("nl-eval"), 0, 0, 0
    for d in rotated_faxes():
        _, out = run(d, rel, gw)
        if out["band"] == "escalate" and out["reason"] == "illegible":
            escal += 1
        elif out["kind"] == "none":
            typed_none += 1
        elif out["kind"] == d.kind:
            right += 1
    return right, escal, typed_none


LAYERS = [Layer(1, "unit", "every function with a rule", "every commit", 60, 0.0),
          Layer(2, "component", "every model step by slice", "every pull request", 900, 2.0),
          Layer(3, "integration", "every boundary", "every pull request", 1200, 0.5),
          Layer(4, "system", "Anne's gold-heldout", "nightly and release", 3600, 12.0),
          Layer(5, "operational", "shadow reconciliation", "daily", 600, 0.0)]


def pyramid(shadow_first_notices_missed):
    """shadow_first_notices_missed(system) -> count, from the shadow reconciliation Ruth Calloway runs."""
    p = Pyramid(LAYERS)
    p.add(1, "C03 policy pattern and check digit, 40 cases", lambda s: (PASS, "40 of 40", 0.4, 0.0, {}))
    p.add(1, "C02 fax header and stamp dates, V-127, 36 cases", lambda s: (PASS, "36 of 36", 0.3, 0.0, {}))
    p.add(1, "claimant 30-character rule, 12 cases", lambda s: (PASS, "12 of 12", 0.1, 0.0, {}))

    def orient(s):
        return (PASS, "48 of 48 pages, 4 angles", 2.1, 0.0, {}) if s["release"].orientation else \
               (PASS, "no detector in this build: test absent", 0.0, 0.0, {})
    p.add(1, "C01 orientation detector", orient)
    p.add(2, "C06 slices, clean scans (T1 to T4, none), 250 docs",
          lambda s: (PASS, "accuracy 0.952, no slice below 0.90", 41.0, 0.07, {}))

    def rot(s):
        if not s["rotated_slice"]:
            return (PASS, "slice not in the suite", 0.0, 0.0, {})
        right, esc, none = c06_slice(s["release"])
        ok = none == 0 and right + esc == 24
        return (PASS if ok else FAIL, f"{right} typed right, {esc} to a clerk as illegible, {none} typed none",
                6.2, 0.01, dict(right=right, escalated=esc, typed_none=none))
    p.add(2, "C06 slice: fax rotated 90/180/270, 24 docs", rot)
    p.add(2, "cw-rules v1 rules as tests, 8 cards x 2 cases", lambda s: (PASS, "16 of 16", 0.8, 0.0, {}))
    p.add(3, "gateway key rotation drill (Sunday 02:00 Eastern)", lambda s: (PASS, "refresh before expiry", 9.0, 0.0, {}))
    p.add(3, "claims-core screens FNOL-1, FNOL-2 fingerprint", lambda s: (PASS, "fingerprints match", 14.0, 0.0, {}))
    p.add(3, "state store: scope, retention and erasure drill", lambda s: (PASS, "3 of 3 drills", 1.2, 0.0, {}))
    p.add(4, "gold-heldout through Anne's gate, 2,010 fields",
          lambda s: (PASS, "84.0%, no stratum below main", 1260.0, 9.40, {}))

    def recon(s):
        n = shadow_first_notices_missed(s)
        return (FAIL if n else PASS, f"{n} first notices keyed by clerks with no agent intake record", 30.0, 0.0,
                dict(missed=n))
    p.add(5, "shadow reconciliation, intake records vs keyed claims", recon)
    return p
