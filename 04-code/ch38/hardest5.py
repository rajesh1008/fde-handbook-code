"""The hardest five questions at pass 3: the claim, the evidence, and the defeaters Sam Oakley raised in the room.
A defeater is a reason the claim could be false. Each one is closed by evidence, by a test run in the room,
or left open and written down as residual risk."""
import _paths  # noqa: F401
from fieldkit.security import evidence_check
import world as W

DEFEATERS = {
    "SQ-30": [("an attack class the red team did not try", "EV-21 covers 6 classes; 2 classes untried", "residual RR-01"),
              ("guardrail v3 tested on the sandbox mix, not live referrals", "EV-21 used 200 sandbox referrals", "condition: rerun on day 160 live sample"),
              ("an injected draft reaches a coordinator who copies it", "coordinator review is the control", "residual RR-01"),
              ("a rule owner leaves", "60 rules, 4 named owners", "closed: owner list in EV-21")],
    "SQ-14": [("the provider switches stored requests back on", "setting in the generated map, every deploy", "closed: EV-23"),
              ("the purge missed a copy", "rescan clean day 124", "closed: EV-24"),
              ("abuse monitoring keeps prompts", "Exhibit C states the terms", "closed: EV-27")],
    "SQ-02": [("a destination added after the map was drawn", "map generated from config, not drawn", "closed: EV-23"),
              ("trace metadata carries patient text", "observed flows reconciled day 114", "condition: rerun before day 144"),
              ("egress opened by the managed-service provider", "default-deny rerun 09:10 day 129", "closed: EV-31")],
    "SQ-26": [("an error path echoes draft text", "F-16 fixed, attack rerun", "closed: EV-21"),
              ("the provider's gateway diagnostics", "diagnostic setting absent from map", "closed: EV-23"),
              ("a reader nobody named", "readers listed in the audit design", "closed: EV-05")],
    "SQ-31": [("a tool call refused but not logged", "F-15 fixed, 4 of 4 logged", "closed: EV-21"),
              ("a new tool added without review", "tool list in the change procedure", "closed: EV-15"),
              ("the allow-list bypassed through the panel", "panel renders text only", "closed: EV-20")],
}
A3 = {a.qid: a for a in W.answers(3)}
ev = {v.qid: v for v in evidence_check(A3.values(), W.EVIDENCE, W.PASS_DAYS[3], W.SCOPE)}
tot = closed = cond = resid = 0
for q in W.HARDEST:
    a = A3[q]
    print(f"{q} [{a.claim}] {a.question}")
    print(f"   answer: {a.text}")
    print(f"   evidence: {', '.join(a.evidence)}; check {'passes' if ev[q].passed else 'fails'}")
    for d, how, fate in DEFEATERS[q]:
        tot += 1; closed += fate.startswith("closed"); cond += fate.startswith("condition"); resid += fate.startswith("residual")
        print(f"   defeater: {d:<52} | {how:<44} | {fate}")
print(f"defeaters raised: {tot}; closed by evidence {closed}; closed by a dated condition {cond}; left as residual risk {resid}")
