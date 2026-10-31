"""Chapter 13 fixtures: Caldwell's sprint zero and sprint 2, Pennant's sprint 2 (the failure injection),
Greystone's first four architecture and control clinics, and key-person holdings on both sides.
Day numbers are engagement days counted from each customer's signature. Every number is invented for the
book's running case and is printed by the lab, so the chapter quotes output, not memory."""
import os, sys, pathlib
sys.path.insert(0, os.environ.get("FIELDKIT_DEV") or str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.cadence import Item, Record, Register

# ---------- Caldwell Mutual: sprint zero (days 15-28) ----------
CALDWELL_COUNTERPARTS = {
    "scope and priority": "Daniel Reyes",
    "extraction acceptance (gold set)": "Anne Kessler",
    "architecture and controls": "Priya Natarajan",
    "operator acceptance (adjuster queue)": "Tom Whitfield",
    "production change approval": "Daniel Reyes",
    "Model-Risk Approval gate": "",            # nobody at Caldwell has said who; sprint zero exposes it
    "Northlight delivery": "Laura Finch",
    "Northlight commercial": "Graham Lowell",
}
CALDWELL_GOLDEN_PATHS = [
    ("GP-1", "emailed first notice with a PDF attachment", "synthetic", 60),
    ("GP-2", "faxed first notice arriving as a multi-page image", "synthetic", 40),
    ("GP-3", "mailed paper form, scanned at the mailroom", "synthetic", 40),
]
CALDWELL_SPRINTS = [("sprint 0", 15, 28), ("sprint 1", 29, 42), ("sprint 2", 43, 56),
                    ("sprint 3", 57, 70), ("sprint 4", 71, 84), ("sprint 5", 85, 98)]

def caldwell_register() -> Register:
    r = Register("Caldwell Mutual")
    r.add(Record("D-01", "Which identity reads claims-core, read-only, and through which path?", "Daniel Reyes",
                 5, 33, kind="access", options=["service role via the gateway account", "replica database"],
                 impact="Architecture Review window day 40-60; shadow start day 100"))
    r.add(Record("D-02", "Where do the 200 sample documents rest, under whose key?", "Priya Natarajan", 47, 49,
                 kind="design", options=["Caldwell bucket, Caldwell key", "Northlight bucket"]))
    r.add(Record("D-03", "How is the review-share claim scored, and by whom?", "Anne Kessler", 15, 22,
                 kind="acceptance"))
    r.add(Record("D-04", "How does the pipeline survive the seven-day gateway key rotation?", "Priya Natarajan",
                 16, 28, kind="design", options=["read key at runtime from Caldwell's secret store", "redeploy weekly"]))
    r.add(Record("D-05", "Which adjusters join the SSO group for the review queue?", "Anne Kessler", 30, 49,
                 kind="access", impact="operator acceptance of the adjuster queue (C-04)"))
    r.add(Record("D-06", "Who at Caldwell approves the Model-Risk Approval gate?", "Daniel Reyes", 22, 42,
                 kind="acceptance", impact="no Model-Risk Approval date can be forecast until named"))
    r.add(Record("D-07", "On what evidence do we continue, re-scope or stop at the day-100 checkpoint?",
                 "Daniel Reyes", 15, 28, kind="stop",
                 options=["continue", "re-baseline once", "stop and close out"]))
    r.add(Record("D-08", "Does C-03 count as accepted while OCR confidence is under 0.80?", "Anne Kessler", 55, 56,
                 kind="acceptance"))
    r.decide("D-03", "Anne's two senior adjusters score 14 fields per document; review share reported beside "
             "field accuracy on auto-routed fields", 20, evidence="repo/decisions/D-03-scoring-rubric-v1.md")
    r.decide("D-04", "Read at runtime from Caldwell's secret store; rotation test before day 54", 26,
             evidence="repo/evidence/rotation-test-day40.log")
    r.decide("D-07", "Continue if claims-core read-only is granted by day 75 and auto-routed field accuracy on "
             "Anne's gold set is at least 95% with review share reported by day 95; otherwise re-baseline "
             "once; a second miss means stop and close out", 28,
             evidence="repo/steering/day28-minute.md", impact="day-100 shadow start depends on it")
    r.decide("D-02", "Caldwell bucket in the claims account, Caldwell-managed key, 90-day retention", 48,
             evidence="repo/clinic/day48-clinic.md")
    r.decide("D-08", "Accepted with follow-up: re-score after the policy-number fix, by day 63", 56,
             evidence="repo/reviews/sprint2-review.md")
    return r

def caldwell_sprint2():
    return [
        Item("C-01", "trace store redacts claimant PII; read only by a Caldwell role", "P0", 5, "Priya Natarajan",
             ["no claimant name, phone or policy number in 200 of 200 sampled traces",
              "only the Caldwell audit role can read the trace bucket"],
             {0: "evidence/redaction-200.txt", 1: "evidence/iam-diff.txt"}, gate="Architecture Review",
             status="accepted"),
        Item("C-02", "gateway key rotation without restart", "P0", 3, "Priya Natarajan",
             ["0 failed calls across the day-54 rotation"], {0: "evidence/rotation-day54.log"},
             gate="Architecture Review", status="accepted"),
        Item("C-03", "extract 14 first-notice fields from the 200 real documents", "P1", 8, "Anne Kessler",
             ["14 fields scored on Anne's gold set, accuracy and review share reported per field"],
             {0: "evidence/goldset-score-v1.csv"}, status="accepted with follow-up", follow_up_day=63,
             follow_up="re-score policy_number after the OCR fix"),
        Item("C-04", "adjuster review queue for low-confidence fields", "P1", 5, "Tom Whitfield",
             ["Tom clears 20 queued documents under his own SSO identity"], {}, status="not accepted",
             blocked_days=9),
        Item("C-05", "readiness check runs before every batch", "P2", 2, "Laura Finch",
             ["a batch with OCR confidence under 0.80 is held and reported"], {0: "evidence/held-batch.txt"},
             status="accepted"),
        Item("C-06", "parallel OCR to cut batch time", "P3", 3, "Laura Finch",
             ["batch of 200 completes in under 6 minutes"], {}),
    ]

# ---------- Pennant Logistics: sprint 2 (days 29-42), Architecture Review booked day 46 ----------
def pennant_sprint2():
    return [
        Item("P-01", "service account scoped to the reconciliation buckets only", "P0", 5, "Jenna Ruiz",
             ["the job's service account has 0 project-wide roles"], {0: "evidence/iam-p01.txt"},
             gate="Architecture Review"),
        Item("P-02", "EU-shipment documents processed and stored only in the EU region", "P0", 8, "Jenna Ruiz",
             ["every document tagged EU is processed and stored in the EU region; 0 copies elsewhere"], {},
             gate="Architecture Review"),
        Item("P-03", "reconcile bills of lading against EDI for the top six layouts", "P1", 5, "Jenna Ruiz",
             ["match rate reported on 300 labeled documents across the 6 layouts"], {0: "evidence/match-300.csv"}),
        Item("P-04", "layout registry shared by parser and scorer", "P2", 3, "Jenna Ruiz",
             ["every one of the 6 layouts has a registry entry with an owner"], {}),
        Item("P-05", "cut parse time from 11 s to 4 s per document for the operations review", "P3", 5,
             "Jenna Ruiz", ["median parse time under 4 s on 300 documents"], {0: "evidence/parse-time.csv"},
             requested_by="Jenna Ruiz"),
    ]

# ---------- Greystone Health: first four clinics (days 30, 33, 37, 40) ----------
# (key, question, raised_by, day, outcome, owner, due_day)  outcome: decision | action | None
GREYSTONE_CLINIC = [
    ("SQ-01", "Where do referral documents rest, and under whose key?", "Sam Oakley", 30, "decision", "Sam Oakley", None),
    ("SQ-02", "Is any protected health information sent outside the Greystone tenant?", "Sam Oakley", 30, "decision", "Sam Oakley", None),
    ("SQ-03", "Who can read traces that contain protected health information?", "Sam Oakley", 30, "action", "Laura Finch", 37),
    ("SQ-04", "Do Northlight engineers get break-glass access to production?", "Sam Oakley", 33, "decision", "Sam Oakley", None),
    ("SQ-05", "Does the business associate agreement cover the model service?", "Sam Oakley", 33, "action", "Marcus Bell", 44),
    ("SQ-06", "Who approves a prompt change on the referral path?", "Sam Oakley", 33, "decision", "Sam Oakley", None),
    ("SQ-07", "How long are drafts retained after a referral closes?", "Sam Oakley", 37, "action", "Michael Hart", 51),
    ("SQ-08", "Where does the audit log go, and in what format?", "Sam Oakley", 37, "action", "Sam Oakley", 41),
    ("SQ-09", "Is there a penetration test before any pilot?", "Sam Oakley", 37, "action", "Sam Oakley", 60),
    ("SQ-10", "How fast is Greystone told about an incident?", "Sam Oakley", 40, "action", "Marcus Bell", 47),
    ("SQ-11", "Which network path does the model call take?", "Sam Oakley", 40, "decision", "Sam Oakley", None),
    ("SQ-12", "Is a model draft ever written into the EHR?", "Sam Oakley", 40, None, "", None),
]

# ---------- key-person holdings (capability -> holders) ----------
HOLDINGS = {
    "Pennant": {
        "approve scope changes": [("Jenna Ruiz", "customer")],
        "accept reconciliation output": [("Jenna Ruiz", "customer")],
        "grant cloud project access": [("Jenna Ruiz", "customer")],
        "explain the 40-plus layouts": [("Jenna Ruiz", "customer"), ("lead FDE", "Northlight")],
        "run the EDI parser": [("lead FDE", "Northlight")],
    },
    "Caldwell": {
        "approve claims-core access": [("Daniel Reyes", "customer")],
        "score the gold set": [("Anne Kessler", "customer")],
        "rotate the gateway key": [("Priya Natarajan", "customer"), ("lead FDE", "Northlight")],
        "operate the adjuster queue": [("Tom Whitfield", "customer")],
        "deploy the pipeline": [("lead FDE", "Northlight")],
    },
}
