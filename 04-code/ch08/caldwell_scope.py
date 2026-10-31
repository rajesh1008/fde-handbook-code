"""Caldwell Mutual's scoping document, days 24 to 28, as data (deterministic stand-in).

Volumes per intake path are the Chapter 6 discovery readout (day 26), frozen here so this lab does not move when
that one does. The document-type mix per path is a labeled stand-in, invented to be consistent with the running
project. Names are the book's roster; no customer data is held.
"""
from __future__ import annotations

from scoping import (Claim, Criterion, DocType, Evidence, Exclusion, OpenDecision, ScopeDoc, Source)

# ------------------------------------------------------------------ discovery data (Chapter 6 readout, day 26)
PATH_VOLUME = {"P01": 4100, "P02": 2300, "P03": 2900, "P04": 2450, "P05": 610, "P06": 540, "P07": 980,
               "P08": 420, "P09": 160, "P10": 230, "P11": 110}
PATH_NAME = {"P01": "paper mail", "P02": "main claims fax", "P03": "claims shared mailbox", "P04": "agent portal",
             "P05": "closed Springfield fax", "P06": "email to an adjuster", "P07": "phone report, papers by mail",
             "P08": "administrator nightly file", "P09": "finance cage mail", "P10": "attorney letters via legal",
             "P11": "repair-estimate platform"}
TYPE_NAME = {"T1": "Caldwell first-notice form", "T2": "agency first-notice form",
             "T3": "first-notice letter or email", "T4": "repair estimate",
             "X1": "attorney letter", "X2": "administrator claim file", "X3": "medical bill or record",
             "X4": "police or fire report", "X5": "photograph or other correspondence"}
# share of each path's documents by type (stand-in, from the shadowing tallies, rounded)
MIX = {
    "P01": {"T1": .45, "T3": .20, "T4": .10, "X3": .10, "X4": .08, "X5": .07},
    "P02": {"T1": .55, "T2": .10, "T3": .10, "T4": .10, "X3": .08, "X4": .07},
    "P03": {"T1": .30, "T3": .35, "T4": .15, "X4": .05, "X5": .15},
    "P04": {"T2": .80, "T4": .10, "X5": .10},
    "P05": {"T1": .50, "T2": .20, "T3": .10, "X3": .10, "X4": .10},
    "P06": {"T3": .55, "T4": .20, "X5": .25},
    "P07": {"T1": .60, "T3": .10, "X3": .15, "X4": .15},
    "P08": {"X2": 1.0},
    "P09": {"T1": .40, "T3": .20, "X5": .40},
    "P10": {"X1": 1.0},
    "P11": {"T4": 1.0},
}


OUT_PATHS = ("P09",)        # finance-cage mail, out of pilot scope by the day-25 decision (Chapter 6)


def type_volumes(skip=OUT_PATHS) -> dict:
    out = {}
    for p, mix in MIX.items():
        if p in skip:
            continue
        for t, s in mix.items():
            out[t] = out.get(t, 0) + round(PATH_VOLUME[p] * s)
    return out


DECISIONS = {
    "K1": "which of the four types this document is, or none",
    "K2": "new claim, or correspondence on an open claim (and which)",
    "K3": "the 14 first-notice fields, drafted into a claim record",
    "K4": "send the drafted fields without review, or to an adjuster",
    "K5": "hold the document when OCR confidence is below 0.80",
}
NEVER = ["coverage", "liability", "reserve amount", "fraud referral", "contact with the claimant",
         "denying or closing a claim"]


def doc_types() -> list:
    v = type_volumes()
    return [DocType("T1", TYPE_NAME["T1"], ("K1", "K2", "K3", "K4", "K5"), v["T1"]),
            DocType("T2", TYPE_NAME["T2"], ("K1", "K2", "K3", "K4", "K5"), v["T2"]),
            DocType("T3", TYPE_NAME["T3"], ("K1", "K2", "K3", "K4", "K5"), v["T3"]),
            DocType("T4", TYPE_NAME["T4"], ("K1", "K2", "K5"), v["T4"])]


def exclusions() -> list:
    v = type_volumes()
    return [Exclusion("attorney letters", "legal privilege; legal owns the route", "legal mail coordinator, as today",
                      v["X1"], revisit="OD-6"),
            Exclusion("finance-cage mail (P09)", "check-bearing letters; finance decides what is a claim (day 25)",
                      "finance cage, as today", PATH_VOLUME["P09"]),
            Exclusion("administrator claim files", "already structured; imported nightly", "existing nightly import",
                      v["X2"]),
            Exclusion("medical bills and records", "never read outside an adjuster (Anne Kessler, day 22)",
                      "attached to the claim unread; adjuster reads", v["X3"]),
            Exclusion("police and fire reports", "no field in the 14 depends on them in release one",
                      "attached to the claim unread", v["X4"]),
            Exclusion("photographs, other correspondence", "not a first notice", "attached unread, or to the "
                      "adjuster's inbox as today", v["X5"])]


def criteria() -> list:
    return [
        Criterion("C-01", "Each document is assigned the right type, or none",
                  "documents with the correct type (T1 to T4, or none)", "Anne Kessler",
                  "Caldwell gold set, stratified by intake path", 500, "all documents in the set", ">= 97%",
                  "suite: type_check, exact match to Anne's label", ("per-type accuracy",)),
        Criterion("C-02", "Correspondence is matched to the right open claim",
                  "matches to the correct open claim", "Anne Kessler",
                  "Caldwell gold set, stratified by intake path", 500, "documents the system matched to a claim",
                  ">= 99.5%", "suite: claim_match, exact match", ("false matches, listed one by one",)),
        Criterion("C-03", "Fields sent to the claims core without review are right",
                  "fields correct, scored under Anne Kessler's rubric", "Anne Kessler",
                  "Caldwell gold set, stratified by intake path", 500,
                  "fields the system sent without review (11 deterministic fields)", ">= 98%",
                  "suite: field_score, exact or rubric match", ("review share", "per-field accuracy")),
        Criterion("C-04", "Adjusters work the review queue faster than keying",
                  "median hands-on minutes per reviewed document", "Tom Whitfield",
                  "golden-path documents, worked under the adjuster's own sign-on", 140,
                  "documents reviewed in the queue", "<= 4.5 min",
                  "queue timer in the review screen", ("documents abandoned to manual keying",)),
        Criterion("C-05", "Unreadable documents are held, never routed",
                  "documents below OCR confidence 0.80 that reached the queue or the claims core",
                  "Priya Natarajan", "every document in shadow weeks", 2000, "documents below 0.80", "= 0",
                  "readiness log join", ("held share by intake path",)),
        Criterion("C-06", "A draft record exists soon after arrival",
                  "documents with a draft record within 15 minutes of arrival, business hours", "Priya Natarajan",
                  "every document in shadow weeks", 2000, "documents arriving 08:00 to 18:00", ">= 95%",
                  "pipeline timestamps against the intake store", ("Monday line",)),
        Criterion("C-07", "Model and compute cost stays under a ceiling",
                  "model and compute charges per document, monthly", "Priya Natarajan",
                  "every document in shadow weeks", 2000, "documents processed", "<= $0.40",
                  "gateway metering export", ("frontier-model share",)),
    ]


# ------------------------------------------------------------------ the open-decision register (day 28)
def register() -> list:
    return [
        OpenDecision("OD-1", "Claims-core read-only access for sampled documents", "Daniel Reyes", 5, 33,
                     "no sampled rung, so no real-data measure of C-02; every gate date moves day for day",
                     ("grant read-only service account", "nightly extract instead"), "access", "D-01"),
        OpenDecision("OD-2", "Who approves the Model-Risk Approval gate", "Daniel Reyes", 15, 42,
                     "no Model-Risk Approval date can be forecast", ("committee chair", "chief risk officer"),
                     "acceptance", "D-06"),
        OpenDecision("OD-3", "Adjuster sign-on group for the review queue", "Anne Kessler", 23, 49,
                     "C-04 cannot be measured under the adjuster's own identity", (), "access", "D-05"),
        OpenDecision("OD-4", "Auto-route threshold: who sets it, and on what evidence", "Anne Kessler", 26, 90,
                     "review share in C-03 is unknown until set; Shadow Exit cannot be planned",
                     ("set from the gold set curve", "fixed at the proposal's 0.90"), "acceptance"),
        OpenDecision("OD-5", "Cause of loss: whose category framework governs when scorers disagree",
                     "Anne Kessler", 27, 35, "cause_of_loss stays outside C-03 until decided",
                     ("Anne rules", "two of three scorers", "report as a range"), "acceptance"),
        OpenDecision("OD-6", "Attorney letters: second release, or never", "Daniel Reyes", 26, 60,
                     "230 documents a month stay manual; a yes adds a privilege review before Build Complete",
                     ("release two", "never"), "scope change"),
        OpenDecision("OD-7", "Cost metering: which gateway export is the source for C-07", "Priya Natarajan", 27, 40,
                     "C-07 has no measurement source until decided", ("gateway usage export", "cloud billing tags"),
                     "design"),
    ]


# ------------------------------------------------------------------ claims in the signed document (v1.0, day 28)
def S(who, party, artifact, day):
    return Source(who, party, artifact, day)


ANNE, DANIEL, PRIYA, TOM = "Anne Kessler", "Daniel Reyes", "Priya Natarajan", "Tom Whitfield"


def claims() -> list:
    v = type_volumes()
    in_scope = v["T1"] + v["T2"] + v["T3"] + v["T4"]
    return [
        # scope
        Claim("S-01", "Intake receives 14,800 documents a month across 11 paths", "R",
              S("intake system report", "customer", "monthly intake counts, Sep", 26), "scope", basis="measured"),
        Claim("S-02", f"The four document types carry {in_scope:,} documents a month", "R",
              S("intake system report", "customer", "monthly intake counts with shadowing mix", 26), "scope",
              basis="estimated"),
        Claim("S-03", "Repair estimates go on the claim; nobody keys them", "F",
              S(ANNE, "customer", "scope working session", 24), "scope"),
        Claim("S-04", "The system drafts the record; fields below threshold go to an adjuster", "P",
              S("Northlight FDE", "vendor", "scope v1.0", 28), "scope"),
        Claim("S-05", "Nothing in release one decides coverage", "F",
              S(DANIEL, "customer", "scope working session", 24), "scope"),
        Claim("S-06", "Four types, five decisions, six never-decisions, as listed", "P",
              S("Northlight FDE", "vendor", "scope v1.0", 28), "scope"),
        # criteria
        Claim("C-a", "Anne Kessler scores extraction; adjusters score under her rubric", "F",
              S(ANNE, "customer", "calibration debrief", 25), "criteria"),
        Claim("C-b", "At least 98% of fields sent without review are right", "F",
              S(DANIEL, "customer", "re-baseline meeting", 12), "criteria", basis="target"),
        Claim("C-c", "Scorers agree on 11 of 14 fields at kappa 0.8 or better", "R",
              S("calibration set scores", "customer", "Anne's calibration sheet", 27), "criteria", basis="measured"),
        Claim("C-d", "Northlight's deal sheet: 95% accuracy", "V",
              S("Graham Lowell", "vendor", "deal sheet", -34), "criteria", basis="target"),
        Claim("C-g", "Gold-set date received is the arrival date on the document's own evidence (stamp, fax header, "
              "mailbox receipt, call log), never the keying date or the scan time", "F",
              S(ANNE, "customer", "calibration alignment session", 25), "criteria"),
        Claim("C-e", "Judge-model checks are not used for acceptance until validated", "P",
              S("Northlight FDE", "vendor", "scope v1.0", 28), "criteria"),
        Claim("OD-4", "Auto-route threshold and who sets it", "D",
              S("Northlight FDE", "vendor", "scope v1.0", 28), "criteria", owner=ANNE, due_day=90),
        Claim("OD-5", "Cause-of-loss framework when scorers disagree", "D",
              S("Northlight FDE", "vendor", "scope v1.0", 28), "criteria", owner=ANNE, due_day=35),
        Claim("C-f", "Proposal: auto-route above 0.90 confidence", "V",
              S("Graham Lowell", "vendor", "deal sheet", -34), "criteria"),
        # volumes, latency, cost
        Claim("V-01", "Monday volume is 1.6 times the weekday mean", "R",
              S("mailroom log", "customer", "mailroom log, 12 weeks", 26), "volumes", basis="measured"),
        Claim("V-02", "A first notice keyed by 3 p.m. is worked the same day", "F",
              S(TOM, "customer", "shadowing session", 19), "volumes"),
        Claim("V-03", "Manual intake costs $7.31 a document", "R",
              S("intake budget", "customer", "Anne's budget and system counts", 26), "volumes", basis="measured"),
        Claim("V-04", "Claims core accepts 20 record writes a minute", "R",
              S("interface specification", "customer", "claims-core interface specification, 2016", 20),
              "volumes", basis="assumed"),
        Claim("V-05", "Model and compute about $0.21 a document", "V",
              S("Northlight FDE", "vendor", "cost model v2", 27), "volumes", basis="estimated"),
        Claim("V-06", "Draft record within 15 minutes of arrival", "P",
              S("Northlight FDE", "vendor", "scope v1.0", 28), "volumes", basis="target"),
        Claim("OD-1", "Claims-core read-only access", "D", S(PRIYA, "customer", "access tracker", 5), "volumes",
              owner=DANIEL, due_day=33),
        Claim("OD-7", "Cost metering source", "D", S(PRIYA, "customer", "scope working session", 27), "volumes",
              owner=PRIYA, due_day=40),
        # out of scope
        Claim("X-01", "Medical records never go through anything but an adjuster", "F",
              S(ANNE, "customer", "scope working session", 22), "out of scope"),
        Claim("X-02", "The administrator file is structured and imported nightly", "R",
              S("import job definition", "customer", "nightly import job, 2019", 21), "out of scope"),
        Claim("X-04", "Legal mail and finance-cage mail stay out of the pilot", "F",
              S(ANNE, "customer", "permission-gap decisions", 25), "out of scope"),
        Claim("X-03", "Attachments that are not first notices are attached unread", "P",
              S("Northlight FDE", "vendor", "scope v1.0", 28), "out of scope"),
        Claim("OD-6", "Attorney letters: second release, or never", "D", S(DANIEL, "customer", "readout", 26),
              "out of scope", owner=DANIEL, due_day=60),
        # register
        Claim("OD-2", "Model-Risk Approval approver", "D", S(DANIEL, "customer", "sprint zero exit", 15),
              "register", owner=DANIEL, due_day=42),
        Claim("OD-3", "Adjuster sign-on group", "D", S(ANNE, "customer", "access tracker", 23), "register",
              owner=ANNE, due_day=49),
        Claim("R-01", "Every open decision has one owner and a due day", "P",
              S("Northlight FDE", "vendor", "scope v1.0", 28), "register"),
    ]


def signed() -> ScopeDoc:
    return ScopeDoc("Caldwell Mutual", 28, "v1.0", doc_types(), DECISIONS, NEVER, criteria(), exclusions(),
                    register(), claims(), signatories=(("Daniel Reyes", "scope and priority"),
                                                       ("Anne Kessler", "scorer, C-01 to C-03"),
                                                       ("Laura Finch", "Northlight delivery")))


# ------------------------------------------------------------------ the earlier documents (failure injection 2)
def lineage() -> dict:
    """A vendor position, three documents later, written as a customer requirement."""
    ds = Claim("DS-07", "Northlight auto-routes every document above 0.90 confidence, no review", "V",
               S("Graham Lowell", "vendor", "deal sheet", -34))
    ko = Claim("KO-12", "Documents above 0.90 confidence go straight to the claims core", "P",
               S("Graham Lowell", "vendor", "kickoff deck", 1), derived_from="DS-07")
    sr = Claim("SR-03", "Caldwell requires auto-routing above 0.90 confidence", "R",
               S("Northlight FDE", "vendor", "week-2 status report", 10), derived_from="KO-12")
    return {c.key: c for c in (ds, ko, sr)}


def draft_v03() -> ScopeDoc:
    """Scope draft v0.3, day 24: the version that went to Daniel for comment."""
    lin = lineage()
    req = Claim("SD-15", "Customer requirement: documents above 0.90 confidence are sent without review", "F",
                S("Caldwell Mutual", "customer", "scope draft v0.3", 24), "criteria", derived_from="SR-03")
    crit = criteria()[:3] + [
        Criterion("C-08", "Accuracy above 95% on Caldwell's documents", metric="accuracy", threshold="> 95%"),
        Criterion("C-09", "Adjusters spend less time on intake", scorer="Anne Kessler",
                  document_set="Caldwell documents"),
    ]
    return ScopeDoc("Caldwell Mutual", 24, "v0.3 draft", doc_types(), DECISIONS, NEVER, crit, exclusions(),
                    register()[:3], [req], lineage=lin)
