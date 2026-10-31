"""fieldkit v2.5 (Chapter 20): estates."""
import pytest
from collections import Counter
from fieldkit.estates import (ModelPin, VersionUnavailable, resolve_pin, resolve_latest, Evidence,
                              conformance, passed, CHECKS, estate_cost, REFUSE_TO_ABSTRACT, PORTS)

CAT = {"us-central1": {"extract": ["extract-2026-01", "extract-2026-04"]},
       "europe-west4": {"extract": ["extract-2025-10", "extract-2026-01"]}}


def test_pin_resolves_where_offered():
    assert resolve_pin(ModelPin("extract", "extract-2026-04", ("us-central1",)), CAT) == ("us-central1", "extract-2026-04")


def test_pin_refuses_substitution():
    with pytest.raises(VersionUnavailable) as e:
        resolve_pin(ModelPin("extract", "extract-2026-04", ("europe-west4",)), CAT)
    assert e.value.elsewhere == ["us-central1"]
    assert [o[0] for o in e.value.options()] == ["wait", "move region", "change the pin"]


def test_latest_silently_substitutes():
    assert resolve_latest("extract", "europe-west4", CAT)[1] == "extract-2026-01"


def test_conformance_all_green_and_counts():
    ev = Evidence("workload", True, True, True, True, True, "us-east-1", ("us-east-1",),
                  Counter({"v": 3}), "v", 0, 0, 3, 3, True, [], [])
    r = conformance(ev)
    assert len(r) == len(CHECKS) == 14 and passed(r) == 14


def test_conformance_off_pin_fails_m2():
    ev = Evidence(served=Counter({"a": 2, "b": 1}), pinned="a", calls=3, records_with_tokens=3)
    m2 = dict((c, ok) for c, ok, _ in conformance(ev))["M2"]
    assert m2 is False


def test_cost_and_scope():
    c = estate_cost(0.02, {"a": 100.0, "b": 100.0}, 10000)
    assert c["fixed_per_doc"] == 0.02 and c["total"] == 0.04 and c["volume_where_fixed_equals_model"] == 10000
    assert len(PORTS) == 5 and len(REFUSE_TO_ABSTRACT) == 5
