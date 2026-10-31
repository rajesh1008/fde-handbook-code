"""Access histories (fieldkit v2, Chapter 15): every request as a dated sequence of events, so a
tracker can be replayed to any day of an engagement, and the day each ladder rung was reached can
be read off rather than remembered. All names are fictional.
"""
import random
from .access import AccessRequest, AccessTracker, LADDER
from .datareadiness import DataReadinessRegister, FieldSpec
from .escalation import EscalationPolicy

# What can be built, and what can be claimed, on each rung of the access ladder.
RUNG_WORK = {
    "synthetic": dict(build=["pipeline skeleton end to end", "schema validators and deterministic rules",
                             "evaluation harness (code, not scores)", "deploy scripts in the sandbox",
                             "tracing and the cost meter", "failure-injection tests"],
                      claim="the plumbing runs; nothing about accuracy"),
    "sampled": dict(build=["readiness report on real files", "profile of real distributions",
                           "gold-set labeling with the customer's experts", "thresholds and routing calibrated",
                           "first measured accuracy, with scorer and documents"],
                    claim="accuracy on a named document set, scored by a named expert"),
    "shadowed": dict(build=["live-volume latency and cost", "freshness and drift checks",
                            "correction review on live work", "comparison with the existing process"],
                     claim="behavior on live work, without acting"),
    "live": dict(build=["write-back actions", "adoption measures", "incident runbooks exercised"],
                 claim="outcomes in production at the agreed volume"),
}


class AccessHistory:
    """Request definitions plus dated events; replay(day) returns the tracker as it stood that day."""

    def __init__(self, customer):
        self.customer = customer
        self.defs = []      # dicts of AccessRequest kwargs (status as first filed)
        self.events = []    # (day, key, changes)

    def define(self, **kw):
        self.defs.append(kw)

    def on(self, day, key, **changes):
        self.events.append((day, key, changes))

    def replay(self, day) -> AccessTracker:
        t = AccessTracker(self.customer)
        for kw in self.defs:
            rd = kw.get("requested_day")
            if rd is not None and rd > day:
                continue
            req = AccessRequest(**kw)
            req.ball_history = [(rd or 0, req.ball)]
            t.add(req)
        for d, key, ch in sorted(self.events, key=lambda e: e[0]):
            if d > day or key not in t.requests:
                continue
            r = t.requests[key]
            for k, v in ch.items():
                setattr(r, k, v)
            if ch.get("status") == "granted":
                r.granted_day = d
            if "ball" in ch:
                r.ball_history.append((d, ch["ball"]))
        return t


def rung_reached_days(tracker):
    """Day each rung was reached: the latest grant among requests on that rung and below."""
    out, latest = {}, 0
    for rung in LADDER:
        on = [r for r in tracker.requests.values() if r.rung == rung]
        if not on or not all(r.status == "granted" for r in on):
            break
        latest = max([latest] + [r.granted_day for r in on])
        out[rung] = latest
    return out


def caldwell_history():
    h = AccessHistory("Caldwell Mutual")
    h.define(key="synthetic-claims-set", what="synthetic claim files built from the schema", rung="synthetic",
             owner="Northlight (us)", requested_day=1, status="requested", ball="us")
    h.define(key="aws-sandbox-account", what="isolated AWS account in Caldwell's org", rung="synthetic",
             owner="Daniel Reyes", requested_day=2, status="requested")
    h.define(key="gateway-key", what="model gateway key", rung="sampled", owner="Priya Natarajan",
             requested_day=4, status="requested", expires_every=7)
    h.define(key="claims-core-readonly", what="read-only service account on the claims core", rung="shadowed",
             owner="Daniel Reyes", requested_day=5, status="in review", next_action="architecture review slot",
             blocks=["integration tests", "shadow feed"])
    h.define(key="claims-sample-200", what="200 de-identified claim files", rung="sampled", owner="Anne Kessler",
             requested_day=9, status="in review", next_action="privacy office intake")
    h.define(key="adjuster-sso-group", what="SSO group for twelve pilot adjusters", rung="shadowed",
             owner="Anne Kessler", requested_day=30, status="requested", next_action="name the twelve adjusters",
             blocks=["shadow feed"])
    h.define(key="sample-storage-decision", what="where the sample is stored and for how long", rung="sampled",
             owner="Priya Natarajan", requested_day=47, status="requested",
             next_action="answer storage question today", blocks=["eval set v1"])
    h.define(key="prod-change-window", what="production change window", rung="live", owner="Daniel Reyes",
             requested_day=None, status="not requested")
    h.on(6, "synthetic-claims-set", status="granted")
    h.on(11, "claims-sample-200", next_action="named readers; bank details redacted first")
    h.on(19, "aws-sandbox-account", status="granted")
    h.on(33, "gateway-key", status="granted")
    h.on(47, "claims-sample-200", status="granted")
    h.on(48, "sample-storage-decision", status="granted")
    h.on(49, "claims-core-readonly", next_action="architecture board on day 54")
    h.on(50, "adjuster-sso-group", status="in review", next_action="SSO change ticket")
    h.on(54, "claims-core-readonly", next_action="platform team creates the role, due day 61")
    return h


def caldwell_policy():
    return EscalationPolicy(
        sponsor="Daniel Reyes", steering="Tuesday steering (Daniel Reyes, Anne Kessler, Priya Natarajan)",
        plan={"eval set v1": 48, "integration tests": 40, "shadow feed": 70},
        asks={"claims-core-readonly": "a slot on the architecture board agenda",
              "sample-storage-decision": "a storage location and retention period for the sample",
              "adjuster-sso-group": "the names of the twelve pilot adjusters"})


def greystone_history():
    h = AccessHistory("Greystone Health")
    h.define(key="synthetic-referrals", what="synthetic referral packets", rung="synthetic",
             owner="Northlight (us)", requested_day=1, status="requested", ball="us")
    h.define(key="azure-subscription", what="Azure subscription with private endpoints", rung="synthetic",
             owner="Sam Oakley", requested_day=3, status="in review", next_action="onboarding review",
             blocks=["deploy", "referral pipeline in tenant"])
    h.define(key="referral-sample", what="de-identified referral packets", rung="sampled", owner="Michael Hart",
             requested_day=10, status="requested", next_action="privacy officer sign-off",
             blocks=["eval set v1"])
    h.on(8, "synthetic-referrals", status="granted")
    h.on(6, "azure-subscription", ball="us", next_action="Northlight answers 26 onboarding security items")
    h.on(47, "azure-subscription", ball="customer", next_action="Sam Oakley reviews the 26 answers")
    h.on(76, "azure-subscription", status="granted")
    h.on(61, "referral-sample", status="in review", owner="privacy officer",
         what="300 de-identified referral packets with a study key",
         next_action="privacy officer review (sponsor Michael Hart)")
    h.on(84, "referral-sample", next_action="minimum necessary: three specialties only")
    h.on(98, "referral-sample", next_action="health-records team extract, due day 104")
    h.on(104, "referral-sample", next_action="redeliver with study key")
    h.on(112, "referral-sample", status="granted")
    return h


def greystone_policy():
    p = EscalationPolicy(
        sponsor="Michael Hart", steering="architecture clinic (Sam Oakley, Michael Hart)",
        plan={"deploy": 30, "referral pipeline in tenant": 45, "eval set v1": 60},
        asks={"azure-subscription": "a date in the architecture clinic to review the 26 answers",
              "referral-sample": "a named approver and a review date for the referral sample"})
    p.record("azure-subscription", 40, 2, "Michael Hart")   # the email that went over Sam Oakley's head
    return p


TRACKER_HISTORIES = dict(caldwell=caldwell_history, greystone=greystone_history)


def caldwell_fields():
    reg = DataReadinessRegister()
    reg.register("caldwell-claims-sample", key="claim_id",
                 required=["policy_number", "loss_date", "doc_type", "pages"],
                 checks={"OCR confidence >= 0.80": lambda r: r.get("ocr_confidence", 0) >= 0.80},
                 min_rows=150)
    reg.register_fields("caldwell-claims-sample", [
        FieldSpec("claim_id", "the claim the file belongs to, as claims core numbers it", "Anne Kessler",
                  supports=("join to gold labels", "deletion proof by key", "duplicate check")),
        FieldSpec("policy_number", "policy in force at loss; blank until coverage is verified", "Anne Kessler",
                  supports=("coverage check",)),
        FieldSpec("loss_date", "date of loss as the claimant reported it", "Tom Whitfield",
                  supports=("late-notice rule",)),
        FieldSpec("doc_type", "intake clerk's label for the document", "Tom Whitfield",
                  supports=("routing by document type",)),
        FieldSpec("pages", "page count after the scanning service splits the file", "Priya Natarajan",
                  supports=("cost per document",)),
        FieldSpec("ocr_confidence", "scanning service's mean character confidence, 0 to 1", "Priya Natarajan",
                  supports=("recognition gate",)),
        FieldSpec("claimant", "claimant name; readers named on the request only", "Anne Kessler",
                  entitlement="named readers only", supports=("claimant match",)),
        FieldSpec("bank_account", "payee bank details", "Anne Kessler", entitlement="redact first",
                  deliver=False),
    ], max_age_days=30)
    return reg


def greystone_sample(n=300, seed=112, drop_key=False):
    """The de-identified referral manifest. study_key is a random code assigned by Greystone, not derived
    from any patient identifier; the mapping stays with Greystone."""
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        row = dict(study_key=f"GS-{rng.getrandbits(40):010x}",
                   specialty=rng.choice(["cardiology", "orthopedics", "gastroenterology"]),
                   urgency=rng.choice(["routine", "routine", "routine", "urgent"]),
                   pages=rng.choice([2, 3, 4, 5, 7, 9, 12]),
                   fax_cover=rng.random() < 0.62,
                   handwritten=rng.random() < 0.18,
                   ocr_confidence=round(rng.betavariate(6, 1.6), 3),
                   received_year=2026)
        if drop_key:
            row.pop("study_key")
        rows.append(row)
    return rows


def greystone_fields():
    reg = DataReadinessRegister()
    reg.register("greystone-referral-sample", key="study_key", required=["specialty", "urgency", "pages"],
                 checks={"OCR confidence >= 0.80": lambda r: r.get("ocr_confidence", 0) >= 0.80},
                 min_rows=250)
    reg.register_fields("greystone-referral-sample", [
        FieldSpec("study_key", "random code per packet; Greystone keeps the mapping", "privacy officer",
                  supports=("join to clinician labels", "deletion proof by key", "re-identification by Greystone")),
        FieldSpec("specialty", "receiving specialty", "Michael Hart", supports=("routing by specialty",)),
        FieldSpec("urgency", "referring clinician's urgency mark", "Michael Hart", supports=("urgent queue rule",)),
        FieldSpec("pages", "pages in the packet", "health-records team", supports=("cost per packet",)),
        FieldSpec("fax_cover", "packet arrived with a fax cover sheet", "health-records team",
                  supports=("cover-sheet stripping",)),
        FieldSpec("handwritten", "any handwritten page", "health-records team", supports=("handwriting route",)),
        FieldSpec("ocr_confidence", "mean character confidence", "health-records team",
                  supports=("recognition gate",)),
        FieldSpec("received_year", "year only, as de-identification requires", "privacy officer"),
        FieldSpec("mrn", "medical record number", "privacy officer", entitlement="never leaves Greystone",
                  deliver=False),
    ], max_age_days=45)
    return reg
