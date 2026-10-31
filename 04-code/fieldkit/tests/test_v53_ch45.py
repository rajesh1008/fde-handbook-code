"""fieldkit v5.3 (Chapter 45): hiring rubric."""
import pytest
from fieldkit.hiring import (Probe, Round, Loop, Score, ScoreRefused, check_score, lint_loop, debrief, calibrate,
                             exact_agreement, discovery_score, classify_score, takehome_validity, five_moves,
                             normalize_round, SELF_REPORT)

O = Probe
LOOP = Loop("t", [Round("A", "a", 45, (O("discovery"), O("build"))), Round("B", "b", 45, (O("discovery"), O("judgment"))),
                  Round("C", "c", 45, (O("decomposition"), O("communication"))), Round("D", "d", 45, (O("build"), O("judgment"))),
                  Round("E", "e", 45, (O("decomposition"), O("communication")))])


def test_balanced_loop_has_no_findings():
    assert lint_loop(LOOP) == []


def test_same_competency_loop_is_flagged():
    bad = Loop("b", [Round(x, x, 60, (O("build"),)) for x in "ABC"] + [Round("D", "d", 45, (Probe("discovery", SELF_REPORT),))])
    codes = [f.code for f in lint_loop(bad)]
    assert codes.count("L1") == 4 and "L3" in codes


def test_takehome_cap():
    lp = Loop("h", LOOP.rounds + [Round("H", "home", 480, (O("build"),), takehome=True)])
    assert any(f.code == "L5" for f in lint_loop(lp))


def test_score_refusals():
    with pytest.raises(ScoreRefused):
        check_score(LOOP, Score("x", "A", "judgment", 3, "asked about trade-offs and the candidate chose one"))
    with pytest.raises(ScoreRefused):
        check_score(LOOP, Score("x", "A", "build", 3, "good"))


def test_debrief_rules():
    ev = "candidate wrote the test before the fix and named the gap"
    s = [Score("i", r, c, 3, ev) for r in "ABCDE" for c in ("discovery", "build", "judgment", "decomposition", "communication")
         if LOOP.round(r).asks(c)]
    assert debrief(LOOP, "c", s).decision == "hire"
    s2 = [x if x.competency != "discovery" else Score("i", x.round, "discovery", 2, ev) for x in s]
    assert debrief(LOOP, "c", s2).decision == "no hire"
    assert debrief(LOOP, "c", s[:-1]).decision == "more evidence"


def test_calibration_offsets():
    r = [(w, s, "build", v) for s in range(4) for w, v in (("a", 3), ("b", 3), ("c", 4))]
    cal = calibrate(r)
    assert cal["c"][0] == 1.0 and cal["a"][0] == 0.0 and exact_agreement(r) == 0.0


def test_discovery_anchor():
    facts = {f"F{i}": i > 8 for i in range(1, 12)}
    assert discovery_score([(2, "question", "F1"), (6, "solution", None)], facts)["anchor"] == 1


def test_classify_and_takehome():
    key = {"a": "deterministic", "b": "human decision"}
    r = classify_score({"a": "frontier model", "b": "frontier model"}, key)
    assert r["over"] == 1 and r["unsafe"] == 1
    assert not takehome_validity([("app", 1.0, True)])["valid"]
    assert takehome_validity([("app", 0.2, True), ("ask", 0.8, False)])["valid"]


def test_five_moves_and_rounds():
    m = five_moves("I gate on the scorer first. At Caldwell it moved 0.60 to 0.90 by day 183. "
                   "That stops being true when the owner leaves. I would show the readiness report.")
    assert all(m.values())
    assert normalize_round("Onsite") == "on-site" and normalize_round("client simulation") == "customer panel"
