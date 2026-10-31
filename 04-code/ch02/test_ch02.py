import pytest
from contracts import CONTRACTS, DEAL_SHEET, FIELD_ESTIMATE
from margin import (year_one, with_, BillingBasisMismatch, gate_days, GATES, Contract, pilot_month_cost,
                    two_year_gross_profit)
from hours_ledger import totals


def test_field_estimate_never_beats_deal_sheet():
    for k, c in CONTRACTS.items():
        assert year_one(c, FIELD_ESTIMATE[k]).margin < year_one(c, DEAL_SHEET[k]).margin


def test_guard_catches_tm_on_fixed():
    with pytest.raises(BillingBasisMismatch):
        year_one(CONTRACTS["pennant"], FIELD_ESTIMATE["pennant"], assume_billing="tm")


def test_tm_assumption_inflates_fixed_deal():
    c, p = CONTRACTS["pennant"], with_(FIELD_ESTIMATE["pennant"], integration_tax=3.0)
    assert year_one(c, p, "tm", strict=False).margin > year_one(c, p).margin + 0.2


def test_tax_lowers_margin_monotonically():
    c, p = CONTRACTS["pennant"], FIELD_ESTIMATE["pennant"]
    ms = [year_one(c, with_(p, integration_tax=t)).margin for t in (0.5, 1, 2, 3)]
    assert ms == sorted(ms, reverse=True)


def test_gates_in_order():
    for plans in (DEAL_SHEET, FIELD_ESTIMATE):
        for p in plans.values():
            d = gate_days(p)
            assert [d[g] for g in GATES] == sorted(d[g] for g in GATES)


def test_deferred_subscription_only_when_start_is_production():
    assert pilot_month_cost(CONTRACTS["caldwell"], FIELD_ESTIMATE["caldwell"])["deferred_subscription"] == 0
    assert pilot_month_cost(CONTRACTS["greystone"], FIELD_ESTIMATE["greystone"])["deferred_subscription"] == 200_000


def test_unknown_bucket_rejected():
    with pytest.raises(ValueError):
        totals([(1, "misc", 5)])


def test_bad_billing_rejected():
    with pytest.raises(ValueError):
        Contract("x", 1, billing="retainer")


def test_never_live_has_no_production_months():
    c, p = CONTRACTS["caldwell"], FIELD_ESTIMATE["caldwell"]
    stuck = with_(p, never_live=True)
    assert year_one(c, stuck).months_to_production is None
    # year one flatters the stuck pilot; the renewal-weighted view does not
    assert year_one(c, stuck).margin > year_one(c, p).margin
    assert two_year_gross_profit(c, stuck)["total"] < two_year_gross_profit(c, p)["total"]
