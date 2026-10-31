"""Section 32.9: three answers written start to finish. Deterministic stand-in (Greystone Health, labeled).

Each answer card holds one claim, its claim type, the evidence ids it rests on, a named owner, and the
observation that would make it false. v1 is the pack as sent on day 100; v2 is the answer as it stood for
the pilot on day 131, after the findings in Section 32.6 closed with retest evidence."""
import dataclasses
import _paths  # noqa: F401
from fieldkit.security import Answer, Evidence, evidence_check
from world import ANSWERS, EVIDENCE, SCOPE, findings

IDS = ("SQ-09", "SQ-26", "SQ-30")
V1 = {a.qid: a for a in ANSWERS if a.qid in IDS}

NEW = {e.id: e for e in [
    Evidence("EV-20", "assessment", "Penetration test of the Greystone deployment, days 116 to 118",
             "Laura Finch", 125, 365, SCOPE),
    Evidence("EV-21", "test output", "Guardrail suite v3 on the injected-instruction red-team set",
             "Sofia Brennan", 128, 90, SCOPE),
    Evidence("EV-22", "test output", "Flow reconciliation from Greystone's exports, 0 undeclared",
             "Erin Walsh", 114, 30, SCOPE),
]}
REG = {**EVIDENCE, **NEW}

V2 = {
    "SQ-09": Answer("SQ-09", V1["SQ-09"].theme, V1["SQ-09"].question,
                    "Yes. An independent firm tested this deployment on days 116 to 118, scoped to the agent and its tools.",
                    ("EV-20",), "measured", V1["SQ-09"].design_changing),
    "SQ-26": Answer("SQ-26", V1["SQ-26"].theme, V1["SQ-26"].question,
                    "Audit records carry identifiers, not text; readers are named; reconciled with your exports.",
                    ("EV-05", "EV-06", "EV-22"), "measured", V1["SQ-26"].design_changing),
    "SQ-30": Answer("SQ-30", V1["SQ-30"].theme, V1["SQ-30"].question,
                    "Drafts cite source spans; uncited text is blocked; the agent has no write tools.",
                    ("EV-21", "EV-20", "EV-03"), "measured", V1["SQ-30"].design_changing),
}
FALSIFIER = {
    "SQ-09": "a report whose scope is not greystone-azure, or a finding in it with no owner",
    "SQ-26": "a pair in the flow logs that the inventory does not declare",
    "SQ-30": "a red-team case whose injected instruction reaches a draft without a block",
}


def show(a, day):
    v = evidence_check([a], REG, day, SCOPE)[0]
    print(f"  {a.qid} [{a.claim}] {a.text}")
    for e in a.evidence:
        ev = REG[e]
        print(f"      {e}  {ev.kind:<12} owner {ev.owner:<14} scope {ev.scope:<16} expires day {ev.expires_day}")
    print(f"      check day {day}: {'PASS' if v.passed else 'FAIL: ' + '; '.join(v.reasons)}")


def finding_for(qid):
    out = []
    for f in findings():
        d = dataclasses.asdict(f) if dataclasses.is_dataclass(f) else vars(f)
        if qid in d.values():
            out.append(f"{d.get('id')} {d.get('severity')} {d.get('kind')}")
    return ", ".join(out) or "none"


print("v1, as sent on day 100 (link check: every answer cites evidence)")
for q in IDS:
    show(V1[q], 100)
    print(f"      finding at review day 103: {finding_for(q)}")
print()
print("v2, as it stood for the pilot on day 131")
for q in IDS:
    show(V2[q], 131)
    print(f"      false if: {FALSIFIER[q]}")
print()
nxt = sorted((REG[e].expires_day, e, q) for q in IDS for e in V2[q].evidence)
print("next expiry among the three cards: day %d (%s, %s)" % nxt[0])
words = {q: (len(V1[q].text.split()), len(V2[q].text.split())) for q in IDS}
print("answer words v1 -> v2: " + ", ".join(f"{q} {a}->{b}" for q, (a, b) in words.items()))
print("claim types v1 -> v2: " + ", ".join(f"{q} {V1[q].claim}->{V2[q].claim}" for q in IDS))
