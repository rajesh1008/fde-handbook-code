"""Greystone's security review, all three passes, as data. Deterministic stand-in for Chapter 38.

Pass 1 (day 103) is the Chapter 32 architecture review, loaded unchanged from 04-code/ch32/world.py.
Pass 2 (day 121) and pass 3 (day 129) are this chapter's. Findings F-13 to F-23 are the eleven raised by the
joint red team of days 126 and 127 (Chapter 36). Evidence EV-23 to EV-30 is new in this chapter.
Days are engagement days. Every number here is a stand-in, not a Greystone measurement."""
import importlib.util, pathlib, hashlib
import _paths  # noqa: F401
from fieldkit.security import Evidence, Answer, Finding, Gate, GateStack

_spec = importlib.util.spec_from_file_location("world32", pathlib.Path(__file__).resolve().parent.parent / "ch32/world.py")
W32 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(W32)

SCOPE = W32.SCOPE
PASS_DAYS = {1: 103, 2: 121, 3: 129}
SIGNOFF_DAY, PILOT_DAY = 130, 131

E = Evidence
NEW_EVIDENCE = [
    E("EV-20", "assessment", "Penetration test of the Greystone deployment (days 116 to 118)", "Laura Finch", 125, 365, SCOPE, "pt-0125"),
    E("EV-21", "test output", "Guardrail v3 red-team rerun, 20 attacks", "Sofia Brennan", 128, 90, SCOPE, "rt-0128"),
    E("EV-22", "test output", "Flow reconciliation, declared against observed", "Erin Walsh", 114, 30, SCOPE, "fr-0114"),
    E("EV-23", "inventory", "Data map generated from deployed configuration", "Sofia Brennan", 128, 30, SCOPE, "c63ad81f3a1a"),
    E("EV-24", "attestation", "Provider stored-request purge confirmation", "Marcus Bell", 124, 365, SCOPE, "pg-0124"),
    E("EV-25", "test output", "Model endpoint outage drill in the sandbox", "Sofia Brennan", 117, 180, SCOPE, "od-0117"),
    E("EV-26", "config export", "Role-scoped trace access export", "Erin Walsh", 115, 90, SCOPE, "rs-0115"),
    E("EV-27", "terms", "Exhibit C, provider retention terms", "Marcus Bell", 120, 365, SCOPE, "xc-0120"),
    E("EV-28", "test output", "Stop switch drill, run desk", "Callum Reid", 111, 180, SCOPE, "ss-0111"),
    E("EV-29", "plan", "Incident response plan v2, named owner", "Laura Finch", 104, 365, SCOPE, "ir-0104"),
    E("EV-30", "test output", "Patient deletion test across store, index, drafts and evaluation set", "Sofia Brennan", 128, 180, SCOPE, "pd-0128"),
    E("EV-31", "test output", "Default-deny egress test rerun, morning of pass 3", "Callum Reid", 129, 30, SCOPE, "eg-0129"),
]
EVIDENCE = dict(W32.EVIDENCE)
for e in NEW_EVIDENCE:
    EVIDENCE[e.id] = e

PASS1 = list(W32.ANSWERS)              # the day-100 pack, as reviewed on day 103
_BY = {a.qid: a for a in PASS1}


def _edit(qid, text=None, evidence=None, claim=None):
    a = _BY[qid]
    return Answer(a.qid, a.theme, a.question, text or a.text, evidence if evidence is not None else a.evidence,
                  claim or a.claim, a.design_changing)


# answers as revised for pass 2 (day 121): the eight findings closed by then, with the evidence that closed them
PASS2_EDITS = {
    "SQ-16": dict(text="One region, westus3; backups in the paired region; failover is a recorded model change.",
                  evidence=("EV-01", "EV-02"), claim="configured"),
    "SQ-18": dict(evidence=("EV-06", "EV-22"), claim="measured"),
    "SQ-10": dict(text="Laura Finch notifies Sam Oakley within 24 hours; the agreement's clock runs from there.",
                  evidence=("EV-29", "EV-10")),
    "SQ-34": dict(text="The run desk disables the agent from the runbook; drilled in 4 minutes.",
                  evidence=("EV-28", "EV-01"), claim="measured"),
    "SQ-26": dict(text="Audit records carry identifiers, not text; prompt bodies redacted; diagnostics in Greystone's workspace.",
                  evidence=("EV-05", "EV-22"), claim="measured"),
    "SQ-03": dict(text="Greystone's platform team reads full traces; Northlight sees redacted traces only.",
                  evidence=("EV-26", "EV-05"), claim="configured"),
    "SQ-33": dict(text="Drafting pauses; referrals continue by hand; drilled in the sandbox.", evidence=("EV-25",),
                  claim="measured"),
    "SQ-14": dict(text="Not for training; abuse monitoring retention is set by Exhibit C.", evidence=("EV-27",),
                  claim="documented"),
}
# answers as revised for pass 3 (day 129)
PASS3_EDITS = {
    # returned at pass 2, closed by the deployment penetration test (EV-20)
    "SQ-09": dict(text="Yes; the deployment was tested days 116 to 118, report issued day 125.", evidence=("EV-20",)),
    "SQ-31": dict(text="Tool allow-list; tested in the deployment penetration test and the red team.",
                  evidence=("EV-20", "EV-21"), claim="measured"),
    "SQ-35": dict(text="Yes; independent penetration test of this deployment, day 125.", evidence=("EV-20",)),
    "SQ-30": dict(text="Input and output guardrails, version 3, 60 rules and 125 tests; red-team rerun day 128; "
                       "one residual risk accepted in writing.", evidence=("EV-21", "EV-20"), claim="measured"),
    # approved at pass 2, changed since (privacy finding P-01, days 122 to 124, and the red team)
    "SQ-02": dict(text="Content goes only to the model service through one private endpoint; trace metadata without "
                       "prompt attributes goes to the observability service.", evidence=("EV-23", "EV-22", "EV-31"),
                  claim="measured"),
    "SQ-14": dict(text="Not for training; stored requests switched off and purged day 124; abuse monitoring per Exhibit C.",
                  evidence=("EV-27", "EV-24", "EV-23"), claim="measured"),
    "SQ-18": dict(evidence=("EV-23", "EV-22"), claim="measured"),
    "SQ-26": dict(text="Audit records carry identifiers, not text; prompt bodies redacted; error messages carry codes only.",
                  evidence=("EV-05", "EV-23", "EV-21"), claim="measured"),
    "SQ-33": dict(text="Drafting pauses; referrals continue by hand; failover drafting waits for a recorded model change.",
                  evidence=("EV-25", "EV-01")),
    "SQ-38": dict(text="Yes, by referral identifier across store, index, drafts and the evaluation set.",
                  evidence=("EV-30",), claim="measured"),
    "SQ-24": dict(evidence=("EV-31",)),
    "SQ-20": dict(text="On behalf of the coordinator; the token ends with the coordinator's session.",
                  evidence=("EV-03", "EV-20"), claim="measured"),
}


def answers(pass_no: int):
    out = {a.qid: a for a in PASS1}
    edits = [PASS2_EDITS] if pass_no >= 2 else []
    if pass_no >= 3:
        edits.append(PASS3_EDITS)
    for ed in edits:
        for q, kw in ed.items():
            _BY_now = out[q]
            out[q] = Answer(q, _BY_now.theme, _BY_now.question, kw.get("text", _BY_now.text),
                            kw.get("evidence", _BY_now.evidence), kw.get("claim", _BY_now.claim), _BY_now.design_changing)
    return [out[a.qid] for a in PASS1]


def morning():
    """Pass 3 answers as they stood at 08:00 on day 129, before the egress test was rerun (EV-04, not EV-31)."""
    return [Answer(a.qid, a.theme, a.question, a.text, tuple("EV-04" if e == "EV-31" else e for e in a.evidence),
                   a.claim, a.design_changing) for a in answers(3)]


def fingerprint(a, register):
    """What the reviewer approved: the answer's words, claim, and the digest of every evidence item it cites."""
    parts = [a.qid, a.text, a.claim] + [f"{e}:{register[e].digest or register[e].issued_day}" for e in a.evidence
                                        if e in register]
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:12]


# ------------------------------------------------------------------------------------------ findings, all 23
RED_TEAM = [  # id, question, severity, summary, owner, closes (day, retest) or None
    ("F-13", "SQ-30", "high", "instruction in a scanned letter's free text changes a draft's summary wording",
     "Sofia Brennan", None),
    ("F-14", "SQ-30", "medium", "instruction on a fax cover sheet shifts the suggested urgency", "Sofia Brennan",
     (128, "EV-21: 0 of 6 cover-sheet attacks shift urgency under v3")),
    ("F-15", "SQ-31", "medium", "a refused tool call is not written to the audit record", "Callum Reid",
     (128, "EV-21: 4 of 4 refused calls in the audit record")),
    ("F-16", "SQ-26", "medium", "draft text echoed into a coordinator error message", "Callum Reid",
     (128, "EV-21: error path returns codes only")),
    ("F-17", "SQ-25", "low", "run record omits the guardrail version", "Sofia Brennan",
     (128, "EV-21: guardrail version in 200 of 200 run records")),
    ("F-18", "SQ-03", "low", "trace sampler keeps full prompts for one percent of runs", "Erin Walsh",
     (128, "EV-23: sampler setting absent from generated map")),
    ("F-19", "SQ-24", "medium", "image link in a referral fetched when the panel renders", "Callum Reid",
     (128, "EV-21: panel renders text only, 0 outbound fetches")),
    ("F-20", "SQ-12", "low", "copy button pastes an approved label with the draft", "Callum Reid",
     (128, "EV-21: copied text carries the draft label")),
    ("F-21", "SQ-33", "medium", "failover region has no model pin, so failover changes the model", "Erin Walsh", None),
    ("F-22", "SQ-38", "low", "patient deletion misses the evaluation set copy", "Sofia Brennan",
     (128, "EV-30: deletion reaches the evaluation set")),
    ("F-23", "SQ-20", "medium", "on-behalf-of token outlives the coordinator's session", "Callum Reid",
     (128, "EV-20 retest: token ends at sign-out")),
]


def findings():
    fs = W32.findings()
    for fid, q, sev, summ, owner, _ in RED_TEAM:
        fs.append(Finding(fid, q, "design", sev, summ, owner, "fix and rerun the attack", 127, 129 if sev == "high" else 140,
                          compensating="draft only; coordinator review; no write tools" if sev == "high" else ""))
    return fs


CLOSURES = list(W32.CLOSURES) + [
    ("F-08", 114, "EV-22: prompt bodies absent from every observed flow"),
    ("F-12", 115, "EV-26: Northlight role sees redacted traces only"),
    ("F-06", 117, "EV-25: endpoint failed in sandbox; drafting paused; referrals continued by hand"),
    ("F-10", 120, "EV-27: Exhibit C signed, abuse monitoring retention stated"),
    ("F-01", 125, "EV-20 issued"), ("F-02", 125, "EV-20: tool authorization retested"), ("F-03", 125, "EV-20 issued"),
    ("F-09", 128, "EV-21: guardrail v3, 19 of 20 attacks stopped, the twentieth is F-13"),
] + [(fid, d, r) for fid, *_, c in RED_TEAM if c for d, r in [c]]

ACCEPTED = {"F-13": "RR-01", "F-21": "RR-02"}

# what the deployed configuration said on each day, for the falsifiers (the observation, not the answer)
OBSERVED = {
    103: dict(outbound={"model service", "observability service"}, prompt_attrs_in_traces=True, stored_requests=True,
              trace_full_sample=0.01, failover_pin=False),
    121: dict(outbound={"model service", "observability service"}, prompt_attrs_in_traces=True, stored_requests=True,
              trace_full_sample=0.01, failover_pin=False),
    129: dict(outbound={"model service", "observability service"}, prompt_attrs_in_traces=False, stored_requests=False,
              trace_full_sample=0.0, failover_pin=False),
}

# the meetings: (topic, minutes)
AGENDA = {1: W32.AGENDA,
          2: [("closed findings, retest evidence", 20), ("open findings and dates", 15), ("red-team scope", 10)],
          3: [("answers changed since pass 2", 15), ("hardest five, defeaters", 25), ("residual risks", 15),
              ("conditions and dates", 5)]}

HARDEST = ["SQ-30", "SQ-14", "SQ-02", "SQ-26", "SQ-31"]


def stack(day: int):
    G = Gate
    if day < PASS_DAYS[2]:
        return [g for s in W32.stacks() if s.customer == "Greystone" for g in s.gates]
    if day < PASS_DAYS[3]:
        return [G("security", "returned", "Sam Oakley", 121), G("model risk", "not started", "Michael Hart"),
                G("procurement", "in review", "Marcus Bell"), G("legal", "in review", "Marcus Bell"),
                G("data protection", "passed", "Hannah Price", 98)]
    if day < SIGNOFF_DAY:
        return [G("security", "in review", "Sam Oakley"), G("model risk", "in review", "Michael Hart"),
                G("procurement", "passed", "Marcus Bell", 127), G("legal", "passed", "Marcus Bell", 127),
                G("data protection", "passed", "Hannah Price", 129)]
    return [G("security", "passed", "Sam Oakley", 130,
              [("rerun flow reconciliation before EV-22 expires", "Erin Walsh", 143),
               ("review RR-01 and RR-02", "Sam Oakley", 190)]),
            G("model risk", "passed", "Michael Hart", 130,
              [("recall at five rechecked on live referrals", "Michael Hart", 160)]),
            G("procurement", "passed", "Marcus Bell", 127), G("legal", "passed", "Marcus Bell", 127),
            G("data protection", "passed", "Hannah Price", 129)]


# the Chapter 14 projection made at scope sign-off (day 19), against what happened
MILESTONES = [("Architecture Review", 94, 103), ("data via provider change", 112, 112), ("pilot", 140, 131)]
BOARD_SLIP_PILOT = 149
