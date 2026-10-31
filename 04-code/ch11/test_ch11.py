import _path  # noqa: F401
import stakeholders as S, champions as C, greystone as G, caldwell, pennant, oakley41, plan, status


def codes(m, today=None):
    return {c for _, c, _ in S.check(m, today)}


def test_kickoff_map_has_no_operator_and_is_not_usable():
    assert "no-operator" in codes(G.KICKOFF)
    assert "blocker-no-reasons" in codes(G.KICKOFF)
    assert S.verdict(G.KICKOFF) == "NOT USABLE"
    assert S.naive_score(G.KICKOFF) == 0.8 and S.gated_score(G.KICKOFF) < 0.5


def test_day12_map_is_usable_and_day40_is_stale():
    assert S.verdict(G.DAY12) == "USABLE"
    stale = [m for lv, c, m in S.check(G.at_day(G.DAY12, G.CONTACT_DAY40, 40)) if c == "stale"]
    assert len(stale) == 3 and any("Luis Ortega" in s for s in stale)


def test_champion_bypass_is_blocked():
    flags = [c for _, c, _ in C.check_register(G.CHAMPIONS, 12)]
    assert flags.count("bypass") == 2


def test_pennant_concentration_and_caldwell_missing_blocker():
    assert "concentration" in codes(pennant.DAY28)
    assert "no-blocker" in codes(caldwell.DAY25)


def test_questions_and_plans():
    assert len(oakley41.QUESTIONS) == 41
    assert sum(q["answered40"] for q in oakley41.QUESTIONS) == 11
    assert plan.design_plan()[1] == 140 and plan.signoff_plan()[1] > 170


def test_status_lint():
    assert len(status.lint(status.DRAFT_W6)) >= 5
    assert status.lint(status.HONEST_W6) == []
