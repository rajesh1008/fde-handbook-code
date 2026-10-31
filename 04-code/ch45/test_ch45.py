"""Chapter 45 lab tests: the numbers the chapter quotes."""
import world as W
from fieldkit.hiring import lint_loop, debrief, discovery_score, classify_score, takehome_validity, calibrate, five_moves


def test_v0_fails_v1_passes():
    assert {f.code for f in lint_loop(W.LOOP_V0)} >= {"L1", "L2", "L3", "L5"} and lint_loop(W.LOOP_V1) == []


def test_debriefs():
    assert debrief(W.LOOP_V1, "c214", W.scores("c214")).decision == "no hire"
    assert debrief(W.LOOP_V1, "c231", W.scores("c231")).decision == "hire"
    d = debrief(W.LOOP_V1, "c236", W.scores("c236"))
    assert d.decision == "more evidence" and len(d.refused) == 2


def test_exercises():
    assert discovery_score(W.TRANSCRIPTS["c214"], W.FACTS)["anchor"] == 1
    assert discovery_score(W.TRANSCRIPTS["c231"], W.FACTS)["anchor"] == 4
    assert classify_score(W.CLASSIFY["c214"], W.STEPS)["unsafe"] == 1
    assert not takehome_validity(W.TAKEHOME["v0"])["valid"] and takehome_validity(W.TAKEHOME["v1"])["valid"]


def test_calibration_and_moves():
    build = lambda w: calibrate([x for x in W.calibration(w) if x[2] == "build"])["Callum Reid"][0]
    assert build("before") >= 0.5 and build("after") < 0.5
    assert sum(five_moves(W.ANSWERS["strong"]).values()) == 5 and sum(five_moves(W.ANSWERS["weak"]).values()) <= 2
