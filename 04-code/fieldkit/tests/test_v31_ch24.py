"""fieldkit v3.1 (Chapter 24): option scoring, fan-out, token broker, mode flag."""
import random
import pytest
from fieldkit.surface import (Option, total, rank, lead, flip_point, weight_draws, Source, run_turn, percentile,
                              Token, TokenBroker, AudienceMismatch, ModeFlag)

W = {"adoption": 50, "governance": 50}
OPTS = [Option("app", "app", {"adoption": 2, "governance": 5}), Option("hyb", "hyb", {"adoption": 5, "governance": 4})]


def test_scores_must_be_one_to_five():
    with pytest.raises(ValueError):
        Option("x", "x", {"adoption": 6})


def test_totals_rank_and_lead():
    assert total(OPTS[1], W) == pytest.approx(90.0)
    assert rank(OPTS, W)[0][0] == "hyb"
    assert lead(OPTS, W, "hyb") == (pytest.approx(20.0), "app")


def test_flip_point_found_on_the_weight_that_matters():
    down, up = flip_point(OPTS, W, "adoption", "hyb")
    assert down is not None and down < 0.35 and up is None


def test_weight_draws_are_seeded():
    assert weight_draws(OPTS, W, n=200, seed=3) == weight_draws(OPTS, W, n=200, seed=3)


def test_parallel_is_bounded_by_slowest_and_timeout_marks_partial():
    srcs = [Source("fast", 100, 0.0), Source("slow", 3000, 0.0)]
    seq = run_turn(srcs, random.Random(1), "sequential", model_ms=0, verify_ms=0, crossing_ms=0)
    par = run_turn(srcs, random.Random(1), "parallel", model_ms=0, verify_ms=0, crossing_ms=0)
    cut = run_turn(srcs, random.Random(1), "parallel", model_ms=0, verify_ms=0, crossing_ms=0, timeout_ms=1000)
    assert seq.fanout_ms == pytest.approx(3100) and par.fanout_ms == pytest.approx(3000)
    assert cut.fanout_ms == pytest.approx(1000) and cut.partial == ["slow"]
    assert percentile([1, 2, 3, 4], 50) == 2.5


def test_broker_refuses_foreign_audience_and_caches():
    b = TokenBroker()
    with pytest.raises(AudienceMismatch):
        b.exchange(Token("u", "https://suite/graph", 0, 3600), "api://claims", 10)
    a = Token("u", "api://nl-brain", 0, 3600)
    t1, ms1 = b.exchange(a, "api://claims", 10)
    t2, ms2 = b.exchange(a, "api://claims", 20)
    assert t1 is t2 and ms1 > ms2 and t1.actor == "nl-brain" and t1.subject == "u"
    _, ms3 = b.exchange(a, "api://claims", 10 + 900 - 30)   # under a minute left: exchange again
    assert ms3 == b.exchange_ms


def test_mode_flag_takes_effect_after_ttl():
    f = ModeFlag("live", ttl_s=30)
    f.set("shadow", 100, "rehearsal")
    assert f.mode_at(110) == "live" and f.mode_at(131) == "shadow"
    with pytest.raises(ValueError):
        f.set("paused", 200, "x")
