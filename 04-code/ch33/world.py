"""Chapter 33 world: Caldwell's claims intake system as components, the frameworks that classify them, the
evidence the evaluation suite already holds, the monitoring metrics and the validator's questions.

Facts carried from earlier chapters are cited by chapter. Nothing here is Caldwell data; the numbers that a later
chapter has not yet fixed are marked [CHECK chNN] in the manuscript, not here.
"""
import _paths  # noqa: F401
from mr import M

C = M.Component
P, D = "prompt", "decision threshold"
STEPS = [  # Chapter 9, Listing 9.x (claims intake, 12 steps)
    C("C01", "receive document, capture text", "code", False, False, False, owner="Priya Natarajan"),
    C("C02", "read received date (stamp, fax header, mail header)", "code", False, False, True, owner="Anne Kessler"),
    C("C03", "parse policy number by pattern and check digit", "code", False, False, True, owner="Anne Kessler"),
    C("C04", "look up policy and coverage in force", "code", False, False, True, owner="Ruth Calloway"),
    C("C05", "match to an existing claim", "code", False, False, True, owner="Ruth Calloway"),
    C("C06", "document type, prompted small model c06-p4", "prompted", True, False, True, True,
      (P, "four signed types", "confidence 0.90 or a person"), "Anne Kessler"),
    C("C07", "loss cause into Caldwell's loss codes, prompted small model", "prompted", True, False, True, True,
      (P, "loss-code table", "confidence 0.85 or a person"), "Anne Kessler"),
    C("C08", "read fixed-zone amounts and dates, validate", "code", False, False, True, owner="Anne Kessler"),
    C("C09", "fast-track and adjuster routing rules", "rules", False, False, True, owner="Anne Kessler"),
    C("C10", "special-investigation referral indicators", "rules", False, False, True, owner="SIU lead"),
    C("C11", "first-notice summary, every statement cited (frontier)", "prompted", True, False, True, True,
      (P, "retrieval over the claims manual", "citation rule"), "Anne Kessler"),
    C("C12", "write claim record and queue item", "code", False, False, True, owner="Ruth Calloway"),
]
EXTRA_82 = [
    C("EX", "field extraction from letters, emails and faxes, prompt p7 on pin extract-2026-04", "prompted", True,
      False, True, True, (P, "ten-field schema", "gold-set gate"), "Anne Kessler", 26),
    C("EM", "embedding model embed-2026-02 for the claims-manual index", "retrieval", True, False, False, True,
      ("index of 6,452 passages", "ACL filter"), "Joan Mercer", 23),
    C("JG", "evaluation judge judge_v2 (scores development runs, never the gold set)", "judge", True, False, False, True,
      (P, "rubric from Anne's rulings"), "Anne Kessler", 26),
]
ROUTER = C("RT", "confidence router v1.1, isotonic correctness model fitted on cal-600 plus 100 broker documents",
           "fitted", True, True, True, False, ("proceed 0.95", "floor 0.47"), "Anne Kessler", 132)
FT = C("C06-ft1", "document type, small model fine-tuned on history-6000 (candidate)", "fine-tuned", True, True, True,
       True, ("training-data record day 138", "guard on absent classes"), "Anne Kessler", 138)

DESIGNS = {82: STEPS + EXTRA_82, 132: STEPS + EXTRA_82 + [ROUTER], 153: STEPS + EXTRA_82 + [ROUTER, FT]}
SYSTEM = C("SYS", "Northlight claims intake system, as one model", "prompted", True, False, True, True, (P,), "")

R = M.Rule
CALDWELL = M.Framework("caldwell-mrm-2026", (
    R({"quantitative": False}, M.NOT_MODEL, "deterministic code or an owned rule set: change control and tests"),
    R({"trained_on_customer_data": True, "core_decision": True}, M.FULL,
      "trained or fitted on Caldwell data for a core decision"),
    R({"core_decision": True}, M.REGISTERED, "third-party model in a core decision: the use is tested, the model is not"),
    R({}, M.TOOL, "supporting tool: inventory entry, owner and a validity check"),
), "Caldwell model-risk policy as signed by Catherine Doyle on day 80")
NORTHLIGHT_V0 = M.Framework("northlight-v0", (
    R({"trained_on_customer_data": True}, M.FULL, "we trained on your data"),
    R({}, M.OUTSIDE, "third-party model, no training on your data"),
), "the vendor's day-76 answer: one question, asked of the whole system")
CALDWELL_V0 = M.Framework("caldwell-v0", (
    R({"quantitative": True}, M.FULL, "artificial intelligence, so tier 1"),
    R({}, M.NOT_MODEL, "not a model"),
), "the day-74 request: the system as one tier-1 model")
HARBOURLINE = M.Framework("harbourline-e23-reading", (
    R({"quantitative": False}, M.NOT_MODEL, "not a model"),
    R({"core_decision": True}, M.FULL, "a model in a material use, vendor or not: risk-rated, validated before use"),
    R({}, M.REGISTERED, "a model in a supporting use: inventoried, low risk rating"),
), "a stand-in reading of a bank policy written to OSFI E-23 [VERIFY]; not Harbourline's text")

E = M.Evidence
S26, S27, S30, S33 = "04-code/ch26/output", "04-code/ch27/output", "04-code/ch30/output", "04-code/ch33/output"
EVIDENCE = [
    E("purpose", "*", "system card: what each component decides, what it never decides (Ch8 scope)", "Callum Reid",
      "signed scope v3", "engagement repo, system-card.md"),
    E("change_control", "*", "pins resolved per estate; a version change is a recorded model change; merge gate with "
      "no override flag", "Priya Natarajan", "gateway version ledger", "Ch18, Ch20, Ch29"),
    E("vendor_due_diligence", "*", "provider system card, model pin, deprecation notice period, incident notice clause",
      "Priya Natarajan", "provider contract schedule 4", "procurement record"),
    E("design_review", "*", "deterministic first, model last: 9 of 12 steps without a model; prompts and retrieval "
      "under the prompt registry", "Callum Reid", "Ch9 classification, Ch23 retrieval design", "Ch9, Ch23"),
    E("limits", "*", "limits register: conditions where a field's accuracy falls more than 10 points", "Sofia Brennan",
      "201 gold-heldout documents, four conditions", f"{S33}/evidence.txt"),
    E("stability", "*", "repeat-run agreement by field, 20 runs at fixed settings", "Sofia Brennan",
      "201 gold-heldout documents", f"{S33}/evidence.txt"),
    E("sensitivity", "*", "accuracy by field under fax noise, rotation and handwriting", "Sofia Brennan",
      "201 gold-heldout documents", f"{S33}/evidence.txt"),
    E("monitoring", "*", "monitoring plan M1 to M6 with thresholds and owners", "Callum Reid", "pack", "pack.md"),
    E("outcomes", "EX", "76.7% of fields correct for p7, corrected by judge_v2 (TPR 0.97, TNR 0.88)", "Anne Kessler",
      "201 gold-heldout documents", f"{S26}"),
    E("outcomes", "C06", "c06-p4 88.4% correct", "Anne Kessler's labelers", "Anne's set, 900 documents", f"{S30}/compare.txt"),
    E("outcomes", "C07", "loss-cause code agreement with the clerk-coded history", "Anne Kessler's labelers",
      "gold-heldout loss_type field", f"{S26}"),
    E("outcomes", "C11", "citation audit: every statement cited, citations checked", "Tom Whitfield", "60 summaries, day 146",
      f"{S33}/review.txt"),
    E("outcomes", "RT", "post-review error 0.9% (36 of 4,000 fields)", "Anne Kessler", "audit-400", f"{S27}/audit.txt"),
    E("conceptual_soundness", "RT", "isotonic correctness model; reliability, ECE and resolution reported", "Callum Reid",
      "cal-600 odd documents", f"{S27}/calibrate.txt"),
    E("development_data", "RT", "cal-600 scored by Tom Whitfield and adjuster B, ties by Anne Kessler; 100 broker "
      "documents day 150", "Tom Whitfield", "600 + 100 shadow documents", f"{S27}/thresholds.txt"),
    E("benchmark", "RT", "v1.1 against v1: lower bound 98.8% on 2,656 proceed fields", "Anne Kessler", "cal-600 odd",
      f"{S27}/drift.txt"),
    E("conceptual_soundness", "C06-ft1", "fine-tune on one closed-set task with an absent-class guard", "Callum Reid",
      "Ch30 design note", f"{S30}"),
    E("development_data", "C06-ft1", "history-6000 under the training-data record signed day 138", "Ruth Calloway",
      "6,000 clerk-coded documents", f"{S30}"),
    E("outcomes", "C06-ft1", "c06-ft1 with guard 93.1% correct", "Anne Kessler's labelers", "Anne's set, 900 documents",
      f"{S30}/compare.txt"),
    E("benchmark", "C06-ft1", "paired against c06-p4 on the same 900 documents", "Anne Kessler's labelers",
      "Anne's set", f"{S30}/compare.txt"),
    E("validity_check", "JG", "judge_v2 TPR 0.97, TNR 0.88 against Anne's labels; weekly 20-document check",
      "Anne Kessler", "201 gold-heldout documents", f"{S26}"),
    E("validity_check", "EM", "question-set recall at 10 by category; ACL drift check", "Joan Mercer",
      "claims-manual question set", "Ch23"),
]

CW, NL = "Caldwell", "Northlight"
I = M.Input
LOG = I("router and decision log", CW, "/caldwell/claims-intake/decisions")
JOB_CW = I("monitoring job", CW, "claims-eval repo, Caldwell CI", runs_as="cw-claims-batch")
JOB_NL = I("monitoring job", CW, "claims-eval repo, Caldwell CI", runs_as="nl-eval")
VENDOR_IDS = ("nl-eval", "nl-shadow", "nl-index")
Mt = M.Metric
M1 = Mt("M1", "proceed-band error, weekly audit sample", "Wilson lower bound at most 2%", "Anne Kessler",
        ("RT", "EX"), (LOG, I("weekly audit labels", CW, "Tom Whitfield's team"), JOB_CW))
M2 = Mt("M2", "router score drift (PSI)", "PSI at most 0.10", "Anne Kessler", ("RT",), (LOG, JOB_CW))
M3 = Mt("M3", "field and type accuracy on the 30-day refresh sample", "at or above the gate line", "Anne Kessler",
        ("EX", "C06", "C06-ft1", "C07"),
        (I("50-document refresh labels", CW, "claims-eval/gold/refresh"), I("scorer", CW, "claims-eval repo"), JOB_CW))
M4_V1 = Mt("M4", "summary and field quality against the reference suite", "at most 2 points below the shadow baseline",
           "Anne Kessler", ("C11", "EX"),
           (I("nl-ref-2400 reference labels", NL, "Northlight AWS account"),
            I("nl-evalkit scorer", NL, "Northlight private package"), JOB_NL))
M4_V2 = Mt("M4", "summary citation audit, 30 summaries a month", "no uncited statement; wrong citations at most 2",
           "Tom Whitfield", ("C11",),
           (I("summaries and cited passages", CW, "/caldwell/claims-intake/decisions"),
            I("audit checklist", CW, "claims procedures, Joan Mercer"), JOB_CW))
M5 = Mt("M5", "pin age and provider deprecation dates", "re-review 30 days before any pin expires", "Priya Natarajan",
        ("EX", "C06", "C07", "C11", "EM", "JG"), (I("gateway version ledger", CW, "Caldwell gateway"), JOB_CW))
M6_V1 = Mt("M6", "judge validity, 20 documents a week", "more than three false passes marks the judge suspect",
           "Anne Kessler", ("JG",), (I("weekly judge labels", CW, "Anne Kessler's labelers"), JOB_NL))
M6_V2 = Mt("M6", M6_V1.name, M6_V1.threshold, "Anne Kessler", ("JG",),
           (I("weekly judge labels", CW, "Anne Kessler's labelers"),
            I("monitoring job", CW, "claims-eval repo, Caldwell CI", runs_as="cw-mrm-monitor")))
METRICS_V1 = [M1, M2, M3, M4_V1, M5, M6_V1]
METRICS_V2 = [M1, M2, M3, M4_V2, M5, M6_V2]

EV, TR, BD = M.EVIDENCE_ANSWER, M.TRANSLATION, M.BOUNDARY
Q = M.ValidatorQuestion
# (one-model framing, component framing): Owen Pritchard's day-74 request, 14 items
REQUEST = [
    ("V01", "Model purpose, use and users", EV, Q("V01", "", EV, "system card and signed scope")),
    ("V02", "Development data description and a sample", BD,
     Q("V02", "", BD, "the frontier model's training data is not available to anyone at Caldwell or Northlight",
       "provider documentation filed; outcome testing on Caldwell's own documents; data for fitted parts supplied")),
    ("V03", "Model specification, equations and coefficients", BD,
     Q("V03", "", BD, "weights are not available; the fitted router and the fine-tune are supplied in full",
       "pinned version; any change is a recorded model change and a re-review")),
    ("V04", "Conceptual soundness of the methodology", BD,
     Q("V04", "", TR, "soundness of the design: decomposition, prompts, retrieval, thresholds and fallbacks")),
    ("V05", "Assumptions and limitations", EV, Q("V05", "", EV, "limits register from the sensitivity runs")),
    ("V06", "Independent replication of the model", BD,
     Q("V06", "", TR, "replicate the system: re-run the evaluation suite in Caldwell CI on the pinned version")),
    ("V07", "Back-testing and outcomes analysis", EV, Q("V07", "", EV, "gold-heldout, Anne's set and audit-400")),
    ("V08", "Benchmarking against a challenger", EV, Q("V08", "", EV, "p7 against the alias; c06-ft1 against c06-p4")),
    ("V09", "Sensitivity analysis", EV, Q("V09", "", EV, "fax noise, rotation and handwriting by field")),
    ("V10", "Stability of the model over time", BD, Q("V10", "", EV, "repeat-run agreement and the drift monitors")),
    ("V11", "Ongoing monitoring with thresholds", EV, Q("V11", "", EV, "M1 to M6, each computable by Caldwell")),
    ("V12", "Change management: what counts as a model change", EV, Q("V12", "", EV, "pins and recorded model changes")),
    ("V13", "The vendor's own validation report for the base model", BD,
     Q("V13", "", BD, "the provider does not issue one to customers",
       "provider system card and evaluation summary filed; notification clause for version changes")),
    ("V14", "Training data for any component trained for Caldwell", EV,
     Q("V14", "", EV, "training-data record for history-6000, signed day 138")),
]

TIMELINE = [  # Caldwell model-risk review, engagement days
    (71, "D-06 decided: Catherine Doyle named as Model-Risk Approval owner (due day 42)"),
    (74, "validation request v0 from Owen Pritchard: one model, tier 1, 14 items"),
    (76, "Northlight answers 'outside scope': one question asked of the whole system"),
    (80, "component test agreed; Caldwell policy written as four rules"),
    (82, "register r1 signed: 15 components, none in full scope"),
    (132, "router fitted on cal-600: register r2, RT enters full scope; OD-4 countersigned"),
    (138, "training-data record signed: register r3, C06-ft1 enters full scope"),
    (140, "pack v1 generated from the evaluation suite: lint clean"),
    (141, "computability check: two of six metrics need Northlight"),
    (144, "pack v2: every metric computable by Caldwell"),
    (146, "validator session: 14 questions answered or bounded"),
    (153, "review passes with two conditions"),
]
