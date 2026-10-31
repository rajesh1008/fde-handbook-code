"""fieldkit v2 (Chapter 15): escalation with dates, field-level readiness register, access histories."""
from fieldkit.fixtures import caldwell_tracker, caldwell_sample
from fieldkit.histories import (caldwell_history, caldwell_policy, greystone_history, greystone_policy,
                                caldwell_fields, greystone_fields, greystone_sample, rung_reached_days, RUNG_WORK)
from fieldkit.escalation import customer_days
from fieldkit.access import LADDER


def test_history_replays_the_day_47_fixture_exactly():
    assert caldwell_history().replay(47).status_report(47) == caldwell_tracker().status_report(47)


def test_day_47_escalations_are_dated_asks_to_owners():
    esc, ours, quiet = caldwell_policy().review(caldwell_history().replay(47), 47)
    keys = {e.key: e for e in esc}
    assert set(keys) == {"claims-core-readonly", "sample-storage-decision"}
    assert all(e.level == 1 and e.to in ("Daniel Reyes", "Priya Natarajan") for e in esc)
    assert keys["claims-core-readonly"].ask_by == 52
    assert keys["sample-storage-decision"].ask_by == 48     # the eval set is planned for day 48
    assert "7 days late" in keys["claims-core-readonly"].note()
    assert any("adjuster-sso-group" in q for q in quiet)


def test_rung_dates():
    assert rung_reached_days(caldwell_history().replay(54)) == {"synthetic": 19, "sampled": 48}
    assert rung_reached_days(greystone_history().replay(112)) == {"synthetic": 76, "sampled": 112}
    assert rung_reached_days(greystone_history().replay(111)) == {"synthetic": 76}


def test_our_move_is_never_escalated():
    esc, ours, _ = greystone_policy().review(greystone_history().replay(40), 40)
    assert any("azure-subscription" in o for o in ours)
    assert "azure-subscription" not in {e.key for e in esc}


def test_customer_days_exclude_our_side():
    r = greystone_history().replay(61).requests["azure-subscription"]
    assert r.days_open(61) == 58 and customer_days(r, 61) == 17


def test_audit_flags_the_day_40_email_and_it_does_not_count():
    pol, t = greystone_policy(), greystone_history().replay(61)
    findings = pol.audit(t)
    assert len(findings) == 2 and "no level 1" in findings[0]
    esc, _, _ = pol.review(t, 61)
    assert {e.key: e.level for e in esc}["azure-subscription"] == 1


def test_key_removed_blocks_and_names_lost_work():
    reg = caldwell_fields()
    ok = reg.assess("caldwell-claims-sample", caldwell_sample(), 41, 47)
    bad = reg.assess("caldwell-claims-sample", caldwell_sample(drop_column="claim_id"), 41, 47)
    assert ok.ready() and not bad.ready() and bad.score < ok.score
    assert any("deletion proof by key" in x for x in bad.lost)


def test_do_not_deliver_field_blocks():
    rows = caldwell_sample()
    for r in rows:
        r["bank_account"] = "000"
    res = caldwell_fields().assess("caldwell-claims-sample", rows, 41, 47)
    assert not res.ready() and any("bank_account" in b for b in res.blocking)


def test_stale_delivery_fails_freshness():
    res = caldwell_fields().assess("caldwell-claims-sample", caldwell_sample(), 1, 47)
    assert any("delivery age 46 days" in f for f in res.failed)


def test_greystone_redelivery_is_ready_and_first_delivery_is_not():
    reg = greystone_fields()
    assert not reg.assess("greystone-referral-sample", greystone_sample(drop_key=True), 99, 104).ready()
    assert reg.assess("greystone-referral-sample", greystone_sample(), 107, 112).ready()


def test_rung_work_covers_the_ladder():
    assert tuple(RUNG_WORK) == LADDER and "accuracy" in RUNG_WORK["synthetic"]["claim"]
