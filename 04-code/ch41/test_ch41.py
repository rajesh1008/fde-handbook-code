"""Chapter 41 lab tests: the numbers the chapter quotes."""
import world as W
from fieldkit.handover import score, without, route_check, lint_runbook, raci_check, path_coverage, drill


def test_caldwell_scores():
    assert score(W.items(W.CALDWELL_BEFORE)).gated == 0.6
    assert score(W.items(W.CALDWELL_AFTER)).gated == 0.9


def test_pennant_score_and_sponsor_dependency():
    it = W.items(W.PENNANT)
    assert score(it).gated == 0.4
    assert score(without(it, "Jenna Ruiz")).gated == 0.3


def test_injected_alert_found():
    assert [a.id for a in route_check(W.ALERTS_V1, W.CW)] == ["A-07"] and not route_check(W.ALERTS_V2, W.CW)


def test_runbooks_and_raci():
    assert sum(len(lint_runbook(r, W.CW_PEOPLE, W.ALERTS_V1)) for r in W.RUNBOOKS_V1) == 4
    assert sum(len(lint_runbook(r, W.CW_PEOPLE, W.ALERTS_V2)) for r in W.RUNBOOKS_V2) == 0
    assert len(raci_check(W.RACI_V1, W.CW_PEOPLE)) == 3 and not raci_check(W.RACI_V2, W.CW_PEOPLE)


def test_paths():
    assert len(path_coverage(W.PATHS_V1, W.NEEDS)) == 3 and not path_coverage(W.PATHS_V2, W.NEEDS)


def test_drills():
    d1 = drill(W.KEY_DRILL, W.ALERTS_V1, W.ROTA, W.RB03_MINUTES, W.CW)
    d2 = drill(W.KEY_DRILL, W.ALERTS_V2, W.ROTA, W.RB03_MINUTES, W.CW)
    assert (d1["passed"], d1["detect"], d1["touches"]) == (False, 115, 1)
    assert (d2["passed"], d2["detect"], d2["mitigate"]) == (True, 6, 38)
    for al in (W.PN_ALERTS_V1, W.PN_ALERTS_V2):
        assert drill(W.PN_DRILL, al, W.PN_ROTA, W.PN_MINUTES, W.PN)["deadline_missed"]
