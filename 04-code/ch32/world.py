"""Greystone Health's security questionnaire pack, evidence register, data flows, threat model and findings.
Deterministic stand-in for Chapter 32. Days are engagement days; negative days are before the engagement began.
Question themes and the 23 design-changing items follow Chapter 11 (04-code/ch11/oakley41.py); SQ-01 to SQ-12
keep the wording recorded in the Chapter 13 clinics."""
import _paths  # noqa: F401
from fieldkit.security import Evidence, Answer, Flow, Threat, ThreatModel, Finding, RemediationPlan, Gate, GateStack

SCOPE = "greystone-azure"
PACK_DAY, REVIEW_DAY = 100, 103

E = Evidence
EVIDENCE = {e.id: e for e in [
    E("EV-01", "design", "Environment design v2 (resubmitted day 97)", "Callum Reid", 97, 180, SCOPE),
    E("EV-02", "config export", "Private endpoint and hub DNS link export", "Erin Walsh", 99, 90, SCOPE),
    E("EV-03", "config export", "Managed identity and on-behalf-of configuration", "Callum Reid", 99, 90, SCOPE),
    E("EV-04", "test output", "Default-deny egress test run", "Callum Reid", 99, 30, SCOPE),
    E("EV-05", "test output", "Audit log design and hash-chain verification", "Sofia Brennan", 98, 90, SCOPE),
    E("EV-06", "inventory", "Data flow inventory v1 (14 flows)", "Sofia Brennan", 100, 90, SCOPE),
    E("EV-07", "assessment", "Penetration test of the drafting agent and its container image", "Laura Finch", -310, 365),
    E("EV-08", "attestation", "SOC 2 Type II report, Northlight", "Laura Finch", -120, 365),
    E("EV-09", "terms", "Model service data, privacy and security terms", "Marcus Bell", 80, 365),
    E("EV-10", "contract", "Business associate agreement coverage of the model service", "Marcus Bell", 44, 730),
    E("EV-11", "design", "Northlight reference architecture for AWS deployments", "Laura Finch", 12, 365,
      "northlight-reference-aws"),
    E("EV-12", "plan", "Incident response plan", "Northlight security team", 20, 365),
    E("EV-13", "decision", "SQ-12 decision: drafts are never written into the EHR", "Michael Hart", 62, 365),
    E("EV-14", "schedule", "Retention schedule for drafts, logs and backups", "Hannah Price", 98, 365),
    E("EV-15", "procedure", "Prompt and model change procedure with approvals", "Sofia Brennan", 95, 180),
    E("EV-16", "procedure", "Access review and leaver procedure", "Erin Walsh", 90, 365),
    E("EV-17", "procedure", "Deletion procedure and certificate template", "Sofia Brennan", 96, 365),
    E("EV-18", "contract", "Master services agreement, subprocessor clause", "Marcus Bell", 30, 730),
    E("EV-19", "design", "Evaluation plan for the drafting agent", "Sofia Brennan", 96, 180),
]}

A = Answer
ANSWERS = [
    # data flow and storage (9; 7 design-changing)
    A("SQ-01", "data flow and storage", "Where do referral documents rest, and under whose key?",
      "In Greystone's storage account in westus3, encrypted with a Greystone-held key.", ("EV-01", "EV-02"), "configured", True),
    A("SQ-02", "data flow and storage", "Is any protected health information sent outside the Greystone tenant?",
      "Only to the model service through one private endpoint; nothing else leaves.", ("EV-02", "EV-04", "EV-06"), "measured", True),
    A("SQ-11", "data flow and storage", "Which network path does the model call take?",
      "Private endpoint in the provider's hub, resolved through the hub DNS zone.", ("EV-02",), "configured", True),
    A("SQ-13", "data flow and storage", "Are documents copied anywhere for indexing or caching?",
      "One index in the tenant; no cache outside it.", ("EV-06",), "configured", True),
    A("SQ-14", "data flow and storage", "Is the model provider allowed to store prompts or completions?",
      "Not for training; the provider's terms describe abuse monitoring.", ("EV-09",), "documented", True),
    A("SQ-15", "data flow and storage", "Where are embeddings stored, and can they be inverted to text?",
      "In the tenant's index, treated as protected health information.", ("EV-06",), "documented", True),
    A("SQ-16", "data flow and storage", "Which region holds every copy of the data?",
      "One region, with backups in the paired region.", ("EV-11",), "documented", True),
    A("SQ-17", "data flow and storage", "Is test or development data drawn from production?",
      "No; development uses the approved sample and synthetic packets.", ("EV-06",), "documented"),
    A("SQ-18", "data flow and storage", "What leaves the tenant in error messages or telemetry?",
      "No document content; error codes only.", ("EV-11",), "documented"),
    # access and identity (8; 6)
    A("SQ-03", "access and identity", "Who can read traces that contain protected health information?",
      "Greystone's platform team and two named Northlight engineers.", ("EV-05",), "configured", True),
    A("SQ-04", "access and identity", "Do Northlight engineers get break-glass access to production?",
      "No standing access; time-bound access approved by Sam Oakley.", ("EV-03", "EV-16"), "configured", True),
    A("SQ-19", "access and identity", "Which identity does the agent use to read the EHR?",
      "A managed identity, no secret held by Northlight.", ("EV-03",), "configured", True),
    A("SQ-20", "access and identity", "Does the agent act on behalf of the coordinator or as itself?",
      "On behalf of the coordinator, with a clinic recheck on release.", ("EV-03",), "configured", True),
    A("SQ-21", "access and identity", "How are secrets stored and rotated?",
      "No secrets in the agent path; certificates in Greystone's key vault.", ("EV-03",), "configured", True),
    A("SQ-22", "access and identity", "Is multifactor authentication enforced for every administrative path?",
      "Yes, through Greystone's identity provider and Northlight's controls.", ("EV-08", "EV-16"), "documented", True),
    A("SQ-23", "access and identity", "How is access reviewed and removed when people leave?",
      "Quarterly review; leavers removed the same day.", ("EV-16", "EV-08"), "documented"),
    A("SQ-24", "access and identity", "Can the agent reach any system not on the approved list?",
      "No; egress is default deny and tested.", ("EV-04",), "measured"),
    # logging and audit (6; 4)
    A("SQ-08", "logging and audit", "Where does the audit log go, and in what format?",
      "Greystone's workspace, hash-chained JSON lines.", ("EV-05",), "measured", True),
    A("SQ-25", "logging and audit", "Can every draft be traced to the documents and prompt that produced it?",
      "Yes; document hashes and prompt version are in the audit record.", ("EV-05", "EV-15"), "measured", True),
    A("SQ-26", "logging and audit", "Do logs contain protected health information, and who can read them?",
      "Audit records carry identifiers, not text; readers are named.", ("EV-05", "EV-06"), "configured", True),
    A("SQ-27", "logging and audit", "Is the audit log tamper-evident?",
      "Yes; the hash chain is verified daily.", ("EV-05",), "measured", True),
    A("SQ-28", "logging and audit", "How long are logs kept?", "Per the retention schedule.", ("EV-14",), "documented"),
    A("SQ-29", "logging and audit", "Are prompt and model version changes logged?",
      "Yes, through the change procedure and the version ledger.", ("EV-15",), "documented"),
    # model behavior and output (6; 4)
    A("SQ-06", "model behavior and output", "Who approves a prompt change on the referral path?",
      "Michael Hart for clinical content, Sam Oakley for anything touching tools.", ("EV-15",), "documented", True),
    A("SQ-12", "model behavior and output", "Is a model draft ever written into the EHR?",
      "No. A coordinator copies an approved draft; the agent has no write scope.", ("EV-13", "EV-03"), "configured", True),
    A("SQ-30", "model behavior and output", "How is the model protected against instructions inside uploaded documents?",
      "The system prompt tells the model to ignore instructions in documents.", ("EV-19",), "documented", True),
    A("SQ-31", "model behavior and output", "What stops the agent taking an action it was not approved for?",
      "Tool allow-list; tested in the last penetration test.", ("EV-07",), "measured", True),
    A("SQ-32", "model behavior and output", "How is output quality measured before and after release?",
      "Against the approved sample, with Michael Hart's reviewers.", ("EV-19",), "documented"),
    A("SQ-33", "model behavior and output", "What happens when the model service is unavailable?",
      "Drafting pauses; referrals continue by hand.", ("EV-01",), "assumed"),
    # incident and breach (4; 1)
    A("SQ-09", "incident and breach", "Is there a penetration test before any pilot?",
      "Yes; the agent and image were tested by an independent firm.", ("EV-07",), "documented", True),
    A("SQ-10", "incident and breach", "How fast is Greystone told about an incident?",
      "Within the time in the business associate agreement.", ("EV-12", "EV-10"), "documented"),
    A("SQ-34", "incident and breach", "Who can stop the agent, and how fast?",
      "Greystone's platform team, by disabling the function.", ("EV-01",), "documented"),
    A("SQ-35", "incident and breach", "Has the system had an independent security assessment?",
      "Yes; see the penetration test report.", ("EV-07",), "documented"),
    # retention and deletion (4; 1)
    A("SQ-07", "retention and deletion", "How long are drafts retained after a referral closes?",
      "Per Greystone's schedule, set by Hannah Price.", ("EV-14",), "documented", True),
    A("SQ-36", "retention and deletion", "How is data deleted at the end of the engagement?",
      "Deleted by Greystone's platform team; certificate issued.", ("EV-17",), "documented"),
    A("SQ-37", "retention and deletion", "Are backups covered by the same retention?", "Yes.", ("EV-14",), "documented"),
    A("SQ-38", "retention and deletion", "Can a single patient's data be deleted on request?",
      "Yes, by referral identifier across store, index and drafts.", ("EV-17",), "documented"),
    # subprocessors and contracts (4; 0)
    A("SQ-05", "subprocessors and contracts", "Does the business associate agreement cover the model service?",
      "Yes, confirmed by Marcus Bell.", ("EV-10",), "documented"),
    A("SQ-39", "subprocessors and contracts", "Which subprocessors touch Greystone data?",
      "The cloud and model provider only.", ("EV-09", "EV-18"), "documented"),
    A("SQ-40", "subprocessors and contracts", "Where is the SOC 2 report for each?",
      "Northlight's and the provider's, in the pack.", ("EV-08",), "documented"),
    A("SQ-41", "subprocessors and contracts", "How are subprocessor changes notified?",
      "Thirty days' notice under the master services agreement.", ("EV-18",), "documented"),
]
ANSWERS.sort(key=lambda a: a.qid)

# ---------------------------------------------------------------------------------------------- data flows
F = Flow
B1, B2, B3 = "internet to tenant", "tenant to model service", "tenant to EHR network"
FLOWS = [
    F("D01", "clinic portal and fax", "intake", "phi", B1, "TLS, sender registry", "portal access log"),
    F("D02", "intake", "document store", "phi", "", "", "storage diagnostic log"),
    F("D03", "document store", "indexer", "phi", "", "", "indexer run log"),
    F("D04", "indexer", "retrieval index", "phi", "", "", "index resource log"),
    F("D05", "orchestrator", "retrieval index", "phi", "", "", "query log"),
    F("D06", "orchestrator", "model endpoint", "phi", B2, "private endpoint, hub DNS", "flow log and DNS answer"),
    F("D07", "orchestrator", "EHR connector", "phi", "", "on-behalf-of token", "token audience in audit"),
    F("D08", "EHR connector", "EHR API", "phi", B3, "read scope, patient filter", "EHR access report"),
    F("D09", "orchestrator", "draft queue", "phi", "", "", "queue metrics"),
    F("D10", "coordinator", "draft queue", "phi", "", "clinic recheck", "approval record"),
    F("D11", "orchestrator", "audit log", "metadata", "", "", "hash-chain check"),
    F("D12", "audit log", "Greystone SIEM", "metadata", "", "", "SIEM ingest count"),
    F("D13", "orchestrator", "key vault", "secret", "", "managed identity", "vault access log"),
    F("D14", "orchestrator", "trace store", "phi", "", "", "workspace query"),
]
OBSERVED = [(f.source, f.dest) for f in FLOWS if f.id != "D12"] + [("orchestrator", "provider diagnostics workspace")]

# ---------------------------------------------------------------------------------------------- threat model
T = Threat
THREATS = ThreatModel("Greystone referral drafting agent", [
    T("T01", "intake", "spoofing", "forged referral from an unknown sender", 3, 3, ("sender registry",), (2, 3)),
    T("T02", "intake", "tampering", "attachment altered after receipt", 2, 3, ("hash at ingest",), (1, 3)),
    T("T03", "intake", "agent misuse", "instructions hidden in an attached document", 4, 4, (), None, "F-09"),
    T("T04", "document store", "information disclosure", "store readable by provider administrators", 2, 5,
      ("customer-held key", "private endpoint"), (1, 5)),
    T("T05", "document store", "tampering", "document replaced in the store", 1, 4, ("immutability policy",), (1, 4)),
    T("T06", "retrieval index", "information disclosure", "embeddings held outside the tenant", 2, 4, ("index in tenant",), (1, 4)),
    T("T07", "retrieval index", "agent misuse", "a poisoned document retrieved for another patient", 2, 4,
      ("index scoped per referral",), (1, 4)),
    T("T08", "orchestrator", "elevation of privilege", "agent identity broader than the coordinator", 3, 5,
      ("on-behalf-of", "clinic recheck"), (1, 5)),
    T("T09", "orchestrator", "agent misuse", "unsafe tool call, such as submitting to a payer", 3, 5,
      ("authorizer refusals",), (1, 5)),
    T("T10", "orchestrator", "denial of service", "runaway loop consumes budget", 3, 2, ("step and cost budgets",), (1, 2)),
    T("T11", "orchestrator", "repudiation", "no record of which prompt produced a draft", 3, 3, ("version in audit",), (1, 3)),
    T("T12", "orchestrator", "agent misuse", "conflicting documents steer the draft", 3, 3,
      ("citations required", "coordinator review"), (2, 3)),
    T("T13", "model endpoint", "information disclosure", "prompts retained for abuse monitoring", 3, 4, (), None, "F-10"),
    T("T14", "model endpoint", "spoofing", "name resolves to a public endpoint", 2, 4, ("hub DNS link",), (1, 4)),
    T("T15", "model endpoint", "denial of service", "model service outage stops drafting", 3, 2, (), None, "F-06"),
    T("T16", "EHR connector", "information disclosure", "reads beyond the referral's patient", 2, 5,
      ("patient-scoped query", "on-behalf-of"), (1, 5)),
    T("T17", "EHR connector", "tampering", "agent writes into the chart", 1, 5, ("no write scope",), (1, 5)),
    T("T18", "draft queue", "agent misuse", "draft presented as clinician-approved", 2, 4, ("draft label", "approval step"), (1, 4)),
    T("T19", "audit log", "tampering", "audit record edited", 2, 4, ("hash chain",), (1, 4)),
    T("T20", "audit log", "repudiation", "coordinator denies an approval", 2, 3, ("delegated identity in log",), (1, 3)),
    T("T21", "trace store", "information disclosure", "prompt text in a diagnostics workspace the provider runs", 4, 4,
      (), None, "F-08"),
    T("T22", "trace store", "information disclosure", "Northlight engineers read traces with patient text", 3, 4, (), None, "F-12"),
])

# ---------------------------------------------------------------------------------------------- findings
def findings():
    Fd = Finding
    return [
        Fd("F-01", "SQ-09", "evidence", "medium", "penetration test expired day 55", "Laura Finch",
           "new test of agent and image in the Greystone deployment", 103, 125),
        Fd("F-02", "SQ-31", "evidence", "medium", "tool allow-list evidence is the expired test", "Laura Finch",
           "retest tool authorization in the new penetration test", 103, 125),
        Fd("F-03", "SQ-35", "evidence", "medium", "independent assessment expired day 55", "Laura Finch",
           "covered by the new penetration test", 103, 125),
        Fd("F-04", "SQ-16", "evidence", "low", "region evidence describes an AWS reference design", "Callum Reid",
           "cite environment design v2 and the backup policy export", 103, 106),
        Fd("F-05", "SQ-18", "evidence", "low", "telemetry evidence describes an AWS reference design", "Callum Reid",
           "cite the data flow inventory and diagnostic settings export", 103, 106),
        Fd("F-06", "SQ-33", "evidence", "low", "outage behavior assumed, never tested", "Sofia Brennan",
           "fail the model endpoint in the sandbox and record what happens", 103, 118),
        Fd("F-07", "SQ-10", "evidence", "low", "incident plan owned by a team, not a person", "Laura Finch",
           "name the incident owner and the notification clock", 103, 106),
        Fd("F-08", "SQ-26", "design", "high", "prompt text reaches a diagnostics workspace the provider runs", "Callum Reid",
           "redact prompt bodies; send diagnostics to Greystone's workspace", 103, 114,
           compensating="diagnostic setting removed day 104"),
        Fd("F-09", "SQ-30", "design", "high", "instructions inside documents reach the drafting step unchecked", "Sofia Brennan",
           "input and output guardrails with tests, then a red team", 103, 128,
           compensating="draft only, no write tools, sandbox read only"),
        Fd("F-10", "SQ-14", "design", "medium", "provider may retain prompts for abuse monitoring", "Marcus Bell",
           "request modified abuse monitoring or record acceptance", 103, 120),
        Fd("F-11", "SQ-34", "design", "medium", "no tested way to stop the agent", "Callum Reid",
           "stop switch in the runbook, tested by the provider's run desk", 103, 112),
        Fd("F-12", "SQ-03", "design", "medium", "Northlight engineers can read traces with patient text", "Erin Walsh",
           "role-scoped traces; Northlight sees redacted traces only", 103, 115),
    ]

CLOSURES = [  # finding, day, retest evidence
    ("F-07", 104, "incident plan v2, owner Laura Finch, 24-hour notice to Sam Oakley"),
    ("F-04", 105, "EV-01 and backup policy export, westus3 and paired region"),
    ("F-05", 105, "EV-06 and diagnostic settings export, error codes only"),
    ("F-11", 111, "stop switch drill: run desk disabled the agent in 4 minutes"),
]
PLANNED = [("F-08", 114), ("F-12", 115), ("F-06", 117), ("F-10", 120), ("F-01", 125), ("F-02", 125),
           ("F-03", 125), ("F-09", 128)]

# ---------------------------------------------------------------------------------------------- gate stacks (Signature 13)
def stacks():
    G = Gate
    return [
        GateStack("Caldwell", [
            G("security", "conditional", "Priya Natarajan", 67,
              [("recheck the load review after the first month of adjuster assist", "Priya Natarajan", 220),
               ("scan in Caldwell's pipeline", "Daniel Reyes", 90)]),
            G("model risk", "not started", "Anne Kessler"), G("procurement", "passed", "Daniel Reyes", 40),
            G("legal", "in review", "Daniel Reyes"), G("data protection", "passed", "Priya Natarajan", 48)]),
        GateStack("Greystone", [
            G("security", "returned", "Sam Oakley", 103), G("model risk", "not started", "Michael Hart"),
            G("procurement", "in review", "Marcus Bell"), G("legal", "in review", "Marcus Bell"),
            G("data protection", "passed", "Hannah Price", 98)]),
        GateStack("Pennant", [
            G("security", "passed", "Kofi Mensah", 60), G("model risk", "not started", "Jenna Ruiz"),
            G("procurement", "passed", "Jenna Ruiz", 30), G("legal", "in review", "Jenna Ruiz"),
            G("data protection", "in review", "Kofi Mensah")]),
        GateStack("Harbourline", [G(n, "not started", "Helen Marsh") for n in
                                  ("security", "model risk", "procurement", "legal", "data protection")]),
    ]

# day each of the 23 design-changing answers was settled (Chapter 11 clinics to the day-103 review)
SETTLED = [30, 30, 30, 33, 33, 33, 37, 37, 40, 40, 40, 62, 75, 89, 89, 89, 89, 97, 103, 103, 103, 103, 103]
# questionnaire size at three customers: asked, applicable, design-changing
SIZES = [("Caldwell", 58, 44, 17), ("Greystone", 41, 41, 23), ("Pennant", 112, 63, 19)]

# the review meeting, day 103 (90 minutes, chaired by Sam Oakley)
AGENDA = [("scope", 10), ("data flow walk", 20), ("threat model", 25), ("contested answers", 25), ("owners and dates", 10)]
PREREAD_ACCEPTED = 27          # answers accepted from the pre-read without discussion
CLEARED_IN_ROOM = ["SQ-12", "SQ-20"]
