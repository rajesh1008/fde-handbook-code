"""Tests for the Chapter 46 lab (deterministic stand-in)."""
import _paths  # noqa: F401
import pytest
from world import ACTUAL, ESTIMATE, CALDWELL_SOURCES, total, tax
import actuals, reserve, phases, waterfall, playbook, price_next, forms, independent


def test_ledgers_and_tax():
    assert total(ACTUAL["caldwell"]) == 3450 and round(tax("caldwell"), 2) == 0.97
    assert round(tax("greystone"), 2) == 2.00 and round(tax("pennant"), 2) == 1.96
    assert sum(CALDWELL_SOURCES.values()) == ACTUAL["caldwell"]["integration"]


def test_factors_use_closed_buckets_only():
    f = actuals.factors()
    assert f["handover"][1] == 1 and round(f["handover"][0], 2) == 1.90
    g = actuals.factors(closed_only=False)
    assert g["handover"][0] < 1.0            # open buckets drag the factor down: the trap the rule prevents


def test_reserve_covers_every_miss():
    m = reserve.misses(); r = reserve.reserve(m)
    assert r == pytest.approx(0.35) and reserve.covered(m, r) == 3
    assert reserve.covered(m, sum(m.values()) / 3 - 1) == 2
    assert reserve.reserve(reserve.misses({"x": 1.45})) == pytest.approx(0.45)


def test_phases():
    g = phases.phase_rows("greystone")
    assert sum(r["rev"] for r in g) == pytest.approx(450_000)          # the cap
    c = phases.phase_rows("caldwell")
    assert sum(r["h"] for r in c) == 3450


def test_waterfall_signature17():
    m = waterfall.main()
    assert 0.40 < m < 0.60 and round(m, 3) == 0.476


def test_transfer_check_failure_injection():
    naive = {s.id for s, ok, _ in playbook.check("next insurer", "naive") if ok}
    checked = {s.id for s, ok, _ in playbook.check("next insurer") if ok}
    assert "PB-04" in naive and "PB-04" not in checked
    assert playbook.credit("next insurer", "naive") - playbook.credit("next insurer") == 120
    assert playbook.credit("greystone") == 390


def test_next_price_meets_target_with_reserve():
    h, r = price_next.priced_hours("checked")
    rh = h["integration"] - h["integration"] / (1 + r)
    fee = price_next.fee_for(h, overrun=rh)
    assert fee == 270_000
    ah, over = price_next.actual_hours(h, r, 1.32)
    assert price_next.year_one(ah, fee, over)[0] >= 0.60


def test_naive_price_misses_target():
    h, r = price_next.priced_hours("naive")
    fee = price_next.fee_for(h, overrun=h["integration"] - h["integration"] / (1 + r))
    ah, over = price_next.actual_hours(h, r, 1.0, price_next.REBUILD)
    assert price_next.year_one(ah, fee, over)[0] < 0.60


def test_outcome_cliff():
    out, *_ = forms.forms()
    k = [n for n in out[1.0][0] if n.startswith("outcome")][0]
    assert out[1.8][0][k] < out[1.5][0][k] - 0.10


def test_independent_collapse():
    assert independent.run(0.0, 1.32, 0)["after"] < 0 < independent.run(0.35, 1.32, 0)["after"]
    assert independent.run(0.35, 1.15, None)["uninsured"] == float("inf")
