import _paths  # noqa: F401
from world import year_one, daily
import fourth


def test_caldwell_matches_ch46():
    assert round(year_one("caldwell")["margin"] * 100, 1) == 47.6
    assert year_one("caldwell")["gp"] == 856_927


def test_greystone_loses_year_one():
    y = year_one("greystone")
    assert y["gp"] < 0 and y["revenue"] == 450_000


def test_pennant_positive_under_signed_form():
    assert year_one("pennant")["margin"] > 0.40


def test_daily_ends_at_year_one():
    for c in ("caldwell", "greystone", "pennant"):
        assert abs(daily(c)[-1] - year_one(c)["gp"]) < 2_000


def test_gate_check_catches_missing_role():
    rows, probs = fourth.check(fourth.SIGNED, {})
    assert any("does not exist in this industry" in p for p in probs)
    assert any("SOX" in p for p in probs)


def test_gate_check_clean_after_map():
    fixed = dict(fourth.SIGNED)
    fixed["Model-Risk Approval"] = ("Rhea Coleman", 152)
    rows, probs = fourth.check(fixed, {"Model-Risk Approval": "accountable executive",
                                       "SOX control owner sign-off": "SOX control owner"})
    assert probs == []
