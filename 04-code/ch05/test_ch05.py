import economics as E
from choose import PROFILES, best, score
from customer_view import totals
from disagreements import LOG, summary
from homes import HOMES
from playbook import INTEGRATOR_PLAYBOOK, VENDOR_PLAYBOOK, run, tally
from reuse import FIXES, route


def test_three_homes_three_fixed_points():
    assert {h.fixed for h in HOMES.values()} == {"the product", "the customer's platform", "the model"}


def test_duration_incentive_signs():
    assert [HOMES[k].duration_sign for k in ("vendor", "integrator", "lab")] == [-1, 1, -1]


def test_vendor_playbook_holds_at_vendor():
    assert tally(run(VENDOR_PLAYBOOK, HOMES["vendor"]))["OK"] == len(VENDOR_PLAYBOOK)


def test_failure_injection_vendor_playbook_at_integrator():
    t = tally(run(VENDOR_PLAYBOOK, HOMES["integrator"]))
    assert t == {"OK": 3, "BENT": 3, "BREAKS": 2, "INVERTS": 2}


def test_repair_holds_at_integrator_only():
    assert tally(run(INTEGRATOR_PLAYBOOK, HOMES["integrator"]))["OK"] == 10
    assert tally(run(INTEGRATOR_PLAYBOOK, HOMES["vendor"]))["OK"] < 10


def test_integration_tax_payers():
    m, i = E.reference_hours()
    assert (m, i) == (700, 840)
    v, integ, lab = E.integration_tax_split(i)
    assert v.employer_net == -126_000 and v.customer_pays == 0
    assert integ.employer_net == 75_600 and integ.customer_pays == 201_600
    assert lab.employer_cost == 31_500 and lab.partner_net == 56_700


def test_extra_month_reuses_ch02():
    rows = {r.home: r for r in E.extra_month_split()}
    assert rows["vendor, fixed fee (Caldwell)"].employer_net == -29_250
    assert rows["vendor, subscription at production (Greystone)"].employer_net == -235_500
    assert rows["integrator, T&M"].employer_net == 15_750


def test_reuse_vendor_counts():
    statuses = [route(f, "vendor")[1] for f in FIXES]
    assert statuses.count("closed: released") == 1 and len(FIXES) == 6


def test_disagreement_log():
    by_axis, kept = summary()
    assert len(LOG) == 14 and sum(by_axis.values()) == 14
    assert kept["neither"] == 6


def test_customer_view_no_home_wins_every_question():
    assert totals() == {"vendor": 4, "integrator": 4, "lab": 6}


def test_each_hire_scores_their_old_home_highest():
    assert best(PROFILES["Callum Reid"])[0] == "integrator"
    assert best(PROFILES["Sofia Brennan"])[0] == "lab"


def test_weights_must_sum_to_one():
    import pytest
    with pytest.raises(AssertionError):
        score([0.5] * 6)
