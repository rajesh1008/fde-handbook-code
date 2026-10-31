import pytest
from fieldkit import AccessRequest, AccessTracker, LADDER, __version__
from fieldkit.fixtures import TRACKERS, CUSTOMERS, caldwell_sample, caldwell_register


def test_version():
    assert __version__.startswith("0.1")


@pytest.mark.parametrize("name", sorted(TRACKERS))
def test_every_customer_fixture_reports(name):
    t = TRACKERS[name]()
    rep = t.status_report(today=47)
    assert CUSTOMERS[name]["name"] in rep
    assert "ladder:" in rep


def test_caldwell_day_47_ladder_is_sampled_not_shadowed():
    t = TRACKERS["caldwell"]()
    assert t.ladder_position() == "synthetic"          # storage decision still open on the sampled rung
    t.grant("sample-storage-decision", 47)
    assert t.ladder_position() == "sampled"


def test_longest_wait_is_named_with_owner():
    t = TRACKERS["caldwell"]()
    first = t.waiting(47)[0]
    assert first.key == "claims-core-readonly" and first.days_open(47) == 42 and first.owner == "Daniel Reyes"


def test_gateway_key_rotation_day():
    t = TRACKERS["caldwell"]()
    assert t.requests["gateway-key"].next_expiry(47) == 54


def test_unknown_rung_rejected():
    with pytest.raises(ValueError):
        AccessRequest("x", "x", "production", "someone", 1)


def test_duplicate_request_rejected():
    t = AccessTracker("X")
    t.add(AccessRequest("a", "a", "synthetic", "o", 1))
    with pytest.raises(KeyError):
        t.add(AccessRequest("a", "a", "synthetic", "o", 1))


def test_sample_ready_but_policy_numbers_short():
    res = caldwell_register().assess("caldwell-claims-sample", caldwell_sample())
    assert res.rows == 200 and res.ready()
    assert any("policy_number" in f for f in res.failed)


def test_failure_injection_key_column_removed_blocks():
    res = caldwell_register().assess("caldwell-claims-sample", caldwell_sample(drop_column="claim_id"))
    assert not res.ready()
    assert any("claim_id" in b for b in res.blocking)


def test_sample_is_reproducible():
    assert caldwell_sample() == caldwell_sample()
    assert LADDER == ("synthetic", "sampled", "shadowed", "live")
