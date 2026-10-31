import pytest
from agent import STEPS, Release, Gateway, run, rotated_faxes, c06_slice, SUITE
from state import ClaimStateStore, Value, ScopeViolation
from walkthrough import EMILY
from world import shadow, CAUSES
import _paths  # noqa: F401
from fieldkit.autonomy import split


def test_split():
    assert list(split(STEPS).values()) == [7, 2, 2, 1]


def test_eight_cards():
    assert len(SUITE.live()) == 8


def test_walkthrough_shadow_no_execute():
    tr, out = run(EMILY, Release(), Gateway(), ClaimStateStore())
    assert "not executed" in tr[-1][3] and out["calls"] == 3


def test_rotated_pre_and_post():
    assert c06_slice(Release(orientation=False, legibility_gate=False))[2] == 24
    assert c06_slice(Release())[2] == 0


def test_shadow_totals():
    d = shadow()
    assert len(d) == 2410 and sum(x["agree"] for x in d) == 2121
    assert sum(not x["agree"] for x in d) == 289 and sum(n or 0 for _, n in CAUSES) == 238


def test_cross_claim_refused():
    st = ClaimStateStore(); st.open("IK-1", "shadow", 1)
    with pytest.raises(ScopeViolation):
        st.put("IK-1", "x", Value("y", "IK-2", "p"), 1)
    with pytest.raises(ScopeViolation):
        st.put_ops("sender_orientation", "s", "text", 1)


def test_hold_blocks_erase():
    st = ClaimStateStore(); run(EMILY, Release(), Gateway(), st)
    st.hold(EMILY.key, 1, "legal", "m")
    assert st.erase(EMILY.key, 2, "r")["erased"] == 0
