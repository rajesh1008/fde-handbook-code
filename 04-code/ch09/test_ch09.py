import pytest
import _path  # noqa: F401
from fieldkit.autonomy import CLASSES, Step, TreeError, walk, split, share, no_model_share
import pipelines as pl
import costs as K
from intake_paths import walk_paths
from parsers import parse_policy, received_date, luhn_digit, Unreadable
import ltv_failure as L


def test_caldwell_split():
    assert [split(pl.CALDWELL)[c] for c in CLASSES] == [7, 2, 2, 1]


def test_three_customers_62_and_79():
    allsteps = pl.CALDWELL + pl.GREYSTONE + pl.PENNANT
    assert len(allsteps) == 52
    assert round(share(allsteps), 2) == 0.62 and round(no_model_share(allsteps), 2) == 0.79


def test_tree_stops_at_first_yes_and_refuses():
    assert walk(Step("a", "x", determined=True, written_rules=True))[0] == 0
    with pytest.raises(TreeError):
        walk(Step("b", "x", written_rules=True))
    with pytest.raises(TreeError):
        walk(Step("c", "x", closed_output=True, check=None))
    with pytest.raises(TreeError):
        walk(Step("d", "x", ops=("arithmetic",)))


def test_finance_cage_refused_until_owned():
    rows = {r[0]: ref for r, _, _, ref in walk_paths()}
    assert rows["P09"] is not None and rows["P01"] is None


def test_volume_weighted_fall_is_71_percent():
    vol = new = demo = 0
    kinds = {"P03": "email", "P06": "email", "P11": "email", "P08": "structured"}
    for row, _, c, _ in walk_paths():
        k = kinds.get(row[0], "scan")
        vol += row[2]; new += row[2] * K.pipeline_cost(c, k)[1]; demo += row[2] * K.demo_cost(k)[1]
    assert round(1 - new / demo, 2) == 0.71


def test_parsers_refuse_not_guess():
    d = "1234567"
    assert parse_policy(f"CM-{d}-{luhn_digit(d)}") == f"CM{d}{luhn_digit(d)}"
    with pytest.raises(Unreadable):
        parse_policy(f"CM-{d}-{(luhn_digit(d) + 1) % 10}")
    with pytest.raises(Unreadable):
        received_date("no stamp here")


def test_ltv_service_is_73_percent_and_cited():
    ltv, lines = L.ltv_service()
    assert round(ltv, 3) == 0.730 and "p3 l12" in lines[0]
