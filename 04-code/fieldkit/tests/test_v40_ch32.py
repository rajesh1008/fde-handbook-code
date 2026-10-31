"""fieldkit v4: security questionnaire as data (Chapter 32)."""
import pytest
from fieldkit.security import (Evidence, Answer, link_check, evidence_check, reuse, expiring, Flow, reconcile_flows,
                               Threat, ThreatModel, Finding, RemediationPlan, review, Gate, GateStack, is_person, AGENT)

REG = {"E1": Evidence("E1", "assessment", "pen test", "Ana Ruiz", -300, 365),
       "E2": Evidence("E2", "design", "env", "Ana Ruiz", 10, 180, "cust-a"),
       "E3": Evidence("E3", "design", "ref", "Ana Ruiz", 10, 180, "ref-aws"),
       "E4": Evidence("E4", "plan", "ir", "security team", 10, 365)}
ANS = [Answer("Q1", "t", "q", "a", ("E1",)), Answer("Q2", "t", "q", "a", ("E2",)),
       Answer("Q3", "t", "q", "a", ("E3",)), Answer("Q4", "t", "q", "a", ("E4",)),
       Answer("Q5", "t", "q", "a", ("E2",), "assumed"), Answer("Q6", "t", "q", "a", ())]


def test_link_check_misses_what_evidence_check_finds():
    assert sum(v.passed for v in link_check(ANS)) == 5
    v = {x.qid: x for x in evidence_check(ANS, REG, 100, "cust-a")}
    assert v["Q2"].passed and not v["Q1"].passed and "expired day 65" in v["Q1"].reasons[0]
    assert "describes ref-aws" in v["Q3"].reasons[0] and "not a person" in v["Q4"].reasons[0]
    assert "assumed" in v["Q5"].reasons[0] and v["Q6"].reasons == ("no evidence",)


def test_reuse_and_expiry():
    assert reuse(ANS)["E2"] == 2
    assert expiring(REG, ANS, 150, 60)[0][1] == "E2"


def test_is_person():
    assert is_person("Sam Oakley") and not is_person("Northlight security team") and not is_person("TBD")


def test_flows():
    fl = [Flow("D1", "a", "b", "phi", "x", "", "log"), Flow("D2", "b", "c", "phi")]
    assert len(fl[0].lint()) == 1 and len(fl[1].lint()) == 1
    r = reconcile_flows(fl, [("a", "b"), ("b", "z")])
    assert r == dict(matched=1, undeclared=[("b", "z")], unseen=["D2"])


def test_threat_model():
    tm = ThreatModel("s", [Threat("T1", "c", "spoofing", "x", 2, 3, ("k",), (1, 3)),
                           Threat("T2", "c", AGENT, "y", 4, 4)])
    assert tm.stride_only() == 1 and [t.id for t in tm.uncontrolled()] == ["T2"]
    assert tm.bands(residual=False)["high"] == 1
    with pytest.raises(AssertionError):
        Threat("T3", "c", "magic", "z", 1, 1)


def test_findings_close_with_retest_only():
    f = Finding("F1", "Q1", "design", "high", "s", "Ana Ruiz", "fix", 100, 140)
    assert "no compensating control" in f.lint()[0]
    with pytest.raises(ValueError):
        f.close(110, "")
    f.close(110, "retest output")
    p = RemediationPlan([f, Finding("F2", "Q2", "evidence", "low", "s", "team", "fix", 100, 105)])
    assert len(p.open_on(111)) == 1 and len(p.overdue(111)) == 1 and len(p.lint()) == 2
    v = evidence_check(ANS[:2], REG, 100, "cust-a")
    assert review(v, [f])["passed"] == 1


def test_gate_stack():
    s = GateStack("c", [Gate("security", "conditional", "Ana Ruiz", 60, [("x", "board", None)]),
                        Gate("legal", "in review", "Ana Ruiz")])
    assert s.blocking() == ["legal"] and len(s.lint()) == 1 and not s.ready()
