"""Chapter 37 world: the gate records as the engagement wrote them. Deterministic, labeled stand-in.

Caldwell numbers are the book's own lab outputs: gold-heldout strata from 04-code/ch31/output/scorecard.txt
(rc-1, day 156; labels by Lena Ortiz, owner Anne Kessler), shadow agreement and audit-shadow-400 from
04-code/ch31/output/shadow_run.txt (days 142 to 153). Field counts per stratum are documents x 10 fields.
Items marked STAND-IN (the draft packet's non-customer evidence, the model-risk component count) are illustrative.
No model calls; no customer data.
"""
import _paths  # noqa: F401
from fieldkit.gates import Criterion, Measurement, GateRecord, Tracker, Artifact, ResidualRisk

DAY = 157
# stratum: (documents, fields right at rc-1); rc-1 percentages match scorecard.txt to one decimal
STRATA = {"first notice, email": (17, 166), "first notice, fax": (50, 372), "first notice, mail": (49, 389),
          "police report": (17, 156), "repair estimate": (17, 154), "medical bill": (17, 152),
          "adjuster note": (17, 151), "photo log": (17, 149)}
P7 = {"first notice, email": 94.7, "first notice, fax": 62.8, "first notice, mail": 69.2, "police report": 87.6,
      "repair estimate": 87.1, "medical bill": 86.5, "adjuster note": 84.1, "photo log": 82.9}
GOLD = "gold-heldout (201 documents, 2,010 fields)"
assert sum(d for d, _ in STRATA.values()) == 201 and sum(k for _, k in STRATA.values()) == 1689

S1 = Criterion("S-1", "field accuracy on gold-heldout", 0.80, per="document class", owner="Anne Kessler")
S2 = Criterion("S-2", "critical fields on gold-heldout", 0.80, owner="Anne Kessler")
S3 = Criterion("S-3", "agreement with keyed claims in shadow", 0.85, owner="Anne Kessler")
S4 = Criterion("S-4", "post-review error, audit-shadow-400", 0.012, higher_is_better=False, owner="Anne Kessler")
S5 = Criterion("S-5", "first notices with no intake record, after the fix", 0.0, higher_is_better=False,
               owner="Ruth Calloway")


def shadow_measurements(per_class=True):
    ms = [Measurement("S-1", 1689, 2010, measured_by="Lena Ortiz (labels), nl-eval CI", on=GOLD, day=156),
          Measurement("S-2", 506, 603, measured_by="Lena Ortiz (labels), nl-eval CI", on=GOLD, day=156),
          Measurement("S-3", 2121, 2410, measured_by="lab code vs production extract", on="shadow days 142-153", day=153),
          Measurement("S-4", 44, 4000, measured_by="Lena Ortiz adjudication", on="audit-shadow-400", day=155),
          Measurement("S-5", 0, 964, measured_by="Ruth Calloway reconciliation", on="intake days 150-153", day=153)]
    if per_class:
        ms += [Measurement("S-1", k, d * 10, scope=c, measured_by="Lena Ortiz (labels)", on=GOLD, day=156)
               for c, (d, k) in STRATA.items()]
    return ms


# STAND-IN: what the first draft of the day-156 packet offered besides customer measurements
DRAFT_EXTRAS = [Measurement("S-1", 91, 100, scope="first notice, fax", kind="model confidence",
                            measured_by="router confidence, mean x100", on="fax first notices, shadow"),
                Measurement("S-1", 1206, 1206, kind="component test", measured_by="Northlight CI",
                            on="unit and integration tests"),
                Measurement("S-3", 1, 1, kind="fluent response", measured_by="summary drafted by a model",
                            on="shadow logs"),
                Measurement("S-4", 0, 2410, kind="log", measured_by="gateway error log", on="shadow days 142-153")]


def caldwell(mode="terms"):
    """mode: 'aggregate' (day-156 packet judged on totals), 'perclass' (same packet, per class), 'terms' (day 157)."""
    t = Tracker("Caldwell Mutual")
    t.add(GateRecord("Architecture Review",
                     entry=[("environment design, data flows and access list", "Chapter 17, day 67")],
                     signer="Priya Natarajan", decided=67,
                     conditions=[("recheck load after the first month of adjuster assist", "Priya Natarajan", 188),
                                 ("module scan runs in Caldwell's pipeline", "Priya Natarajan", 141)]))
    t.add(GateRecord("Build Complete",
                     entry=[("Architecture Review passed", "day 67"), ("load test 20 writes/min vs 9.1 needed", "Chapter 8")],
                     criteria=[Criterion("B-1", "evaluation suite reports per class in Caldwell CI", 1.0, outcome=False),
                               Criterion("B-2", "load test sustained at the needed rate", 1.0, outcome=False),
                               Criterion("B-3", "environment conditions owned and dated", 1.0, outcome=False)],
                     measurements=[Measurement("B-1", 1, 1, kind="component test", measured_by="Sofia Brennan", day=141),
                                   Measurement("B-2", 1, 1, kind="component test", measured_by="Priya Natarajan", day=140),
                                   Measurement("B-3", 2, 2, measured_by="Priya Natarajan", day=141)],
                     signer="Priya Natarajan", decided=141))
    sx = GateRecord("Shadow Exit",
                    entry=[("Build Complete passed", "day 141"), ("shadow window days 142-153, 2,410 documents", "Ch31"),
                           ("adjudication days 154-155", "Lena Ortiz")],
                    criteria=[S1, S2, S3, S4, S5], measurements=shadow_measurements(mode != "aggregate"))
    if mode == "terms":
        sx.signer, sx.decided = "Anne Kessler", 157
        sx.excluded = [("S-1", "first notice, fax", "Anne Kessler", 157)]
        sx.accepted = [("S-1", "first notice, mail", "Anne Kessler", 157)]
        sx.conditions = [("fax first notices route to review until a fresh gold sample meets 80%", "Anne Kessler", 190),
                         ("mail first notices re-measured on a fresh gold sample", "Lena Ortiz", 190)]
    else:
        sx.signer, sx.decided = "Anne Kessler", 156
    t.add(sx)
    t.add(GateRecord("Model-Risk Approval",
                     entry=[("register r3, 17 components", "Chapter 33"), ("threshold record OD-4", "day 132")],
                     criteria=[Criterion("M-1", "components validated or kept off (STAND-IN count)", 1.0, outcome=False)],
                     measurements=[Measurement("M-1", 17, 17, measured_by="Owen Pritchard", day=153)],
                     signer="Catherine Doyle", decided=153,
                     conditions=[("R1: C06-ft1 validated before it is switched on", "Owen Pritchard", 190),
                                 ("R2 (Chapter 33)", "Anne Kessler", 190)]))
    return t


def others():
    """Five-gate rows for Signature 13 (status, day); each customer's own engagement days."""
    return [("Caldwell", None),
            ("Greystone", [("passed", 129), ("in review", None), ("not started", None), ("not started", None),
                           ("not started", None)]),
            ("Pennant", [("passed", 60), ("in review", None), ("not started", None), ("not started", None),
                         ("not started", None)]),
            ("Harbourline", [("not started", None)] * 5)]


ACCOUNTABLE = [
    ("Caldwell Mutual", "insurer", "Anne Kessler, Head of Claims", "Catherine Doyle, Head of Model Risk",
     "claims intake fields and routing; never coverage or reserves"),
    ("Greystone Health", "hospital", "Denise Alvarez, VP Ambulatory Operations", "Michael Hart, CMIO (clinical rule)",
     "draft-only referral intake and prior-authorization drafts"),
    ("Pennant Logistics", "logistics firm", "Jenna Ruiz, VP Operations", "finance controller (two-outcome policy)",
     "freight-audit match proposals; Dana Whitaker owns 'matched'"),
    ("Harbourline Bank", "bank", "David Okafor (named at bid)", "Helen Marsh, Head of Model Risk",
     "not yet scoped; bid stage")]


def pack_logs():
    """What existed on day 141 when Anne Kessler asked what she would show a regulator: logs."""
    return [Artifact("decision record", "decision register (Chapter 13)", "", None, "partial",
                     "decisions exist; none linked to the version they approved"),
            Artifact("lineage", "run records, hash chain", "Priya Natarajan", 141, "partial",
                     "document to field, but not to the gold-set version"),
            Artifact("model and prompt versions", "deploy logs", "", None, "partial", "in logs, no single record"),
            Artifact("evaluation at the time", gap="last number in slides (p7, day 94)"),
            Artifact("human review", gap="review band defined, no adjudicated sample yet"),
            Artifact("authority boundary", gap="in the design, not signed by the business owner"),
            Artifact("incident history", "gateway error log", "", None, "partial", "errors, no write-ups"),
            Artifact("monitoring", gap="dashboards, no thresholds or owners")]


def pack_day157():
    return [Artifact("decision record", "D-06 d71; OD-4 d132 (Catherine Doyle); v1.1 d151; Shadow Exit d157",
                     "Anne Kessler", 157, "present"),
            Artifact("lineage", "run records to gold-heldout v of day 156", "Priya Natarajan", 156, "present"),
            Artifact("model and prompt versions", "rc-1; router v1.1; register r3", "Owen Pritchard", 156, "present"),
            Artifact("evaluation at the time", "gold-heldout per class; audit-shadow-400", "Anne Kessler", 156, "present"),
            Artifact("human review", "Lena Ortiz adjudication, days 154-155", "Lena Ortiz", 155, "present"),
            Artifact("authority boundary", "fields and routing only; proceed 0.95, floor 0.47", "Anne Kessler", 151,
                     "present"),
            Artifact("incident history", "rotated fax days 142-149, fixed day 150", "Ruth Calloway", 153, "present"),
            Artifact("monitoring", "M1 drift alarm (day 149)", "Owen Pryce", 149, "partial",
                     "no per-class monitor for fax and mail yet")]


def residual(version):
    if version == "v1":   # draft of day 156
        return [ResidualRisk("fax first notices below the 80% bar", "Anne Kessler", 157, 190, "route to review"),
                ResidualRisk("mail first notices: interval spans the bar", "Anne Kessler", 157, 190,
                             "weekly per-class audit sample"),
                ResidualRisk("S-4 interval upper end 1.47% above 1.2%", "the business", 157, 190, "audit sample"),
                ResidualRisk("C06-ft1 unvalidated (R1)", "Catherine Doyle", 153, 190, "component switched off"),
                ResidualRisk("fine-tuned weights retention open", "Elaine Porter", 149, None, "")]
    return [ResidualRisk("fax first notices below the 80% bar", "Anne Kessler", 157, 190, "route to review"),
            ResidualRisk("mail first notices: interval spans the bar", "Anne Kessler", 157, 190,
                         "weekly per-class audit sample"),
            ResidualRisk("S-4 interval upper end 1.47% above 1.2%", "Anne Kessler", 157, 190, "audit sample"),
            ResidualRisk("C06-ft1 unvalidated (R1)", "Catherine Doyle", 153, 190, "component switched off"),
            ResidualRisk("fine-tuned weights retention open", "Elaine Porter", 157, 190, "no new fine-tune runs")]
