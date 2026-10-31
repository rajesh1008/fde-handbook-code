import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import weeklog as W
from fieldkit.fixtures import caldwell_tracker

D = pathlib.Path(__file__).resolve().parent / "data"


def test_caldwell_week_is_ok():
    a = W.load(D, "week_a_caldwell", "caldwellmutual.com")
    share, flags, label = W.verdict(a, tracker=caldwell_tracker())
    assert label == "OK" and flags == [] and round(share, 2) == 0.29
    assert sum(a.hours.values()) == 36.0


def test_injected_week_is_caught():
    a = W.load(D, "week_a_caldwell", "caldwellmutual.com")
    b = W.load(D, "week_b_injected", "caldwellmutual.com")
    share, flags, label = W.verdict(b, baseline=a, tracker=caldwell_tracker())
    assert label.startswith("PRODUCTIVE-LOOKING") and share == 0
    assert any("day 89" in f for f in flags)
    assert sum(b.commits.values()) == 41 and b.tickets_closed == 19


def test_rotation_days_from_fieldkit():
    assert W.rotation_days(range(81, 86), caldwell_tracker()) == [82]
    assert W.rotation_days(range(88, 93), caldwell_tracker()) == [89]


def test_second_customer_domains():
    one = W.load(D, "week_c_greystone", "greystonehealth.org")
    both = W.load(D, "week_c_greystone", ("greystonehealth.org", "greystone-msp.net"))
    assert sum(one.contact.values()) == 2.5 and sum(both.contact.values()) == 8.0


def test_calendar_hours_not_double_counted():
    a = W.load(D, "week_a_caldwell", "caldwellmutual.com")
    assert sum(a.hours.values()) == sum(W.hours(r[1], r[2]) for r in __import__("make_weeks").WEEK_A_CAL)
