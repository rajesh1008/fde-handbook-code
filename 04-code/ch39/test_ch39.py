import _paths  # noqa: F401
from collections import Counter
import world as W, suite as U

D = W.caldwell_window()


def test_window_matches_chapter_31():
    assert W.agreement(D)[:2] == (2121, 2410)
    c = Counter(x["cause"] for x in D if x["cause"])
    assert c == {"other agent error": 125, "equivalent format": 61, "clerk keying error, agent right": 52,
                 "broker template, date received": 38, "rotated fax, no intake record": 13}
    assert Counter(x["band"] for x in D) == {"proceed": 1494, "review": 714, "escalate": 189, "none": 13}
    for d in W.DAYS:
        assert sum(1 for x in D if x["day"] == d and x["cause"] is None) == W.AGREE[d]


def test_funnel_conserves_documents():
    f = U.funnel(D)
    assert f["agree"] + f["equivalent"] + f["human_wrong"] + f["agent_wrong"] == f["seen"]
    assert f["loud"] + f["silent"] == f["agent_wrong"] == 176


def test_caldwell_goes_with_conditions():
    rows, dec, _ = U.gate(D)
    assert dec == "GO WITH CONDITIONS"
    assert {r[0]: r[4] for r in rows}["G-5"] == "condition"


def test_holiday_injection_fools_naive_rule_not_gate():
    _, _, since = U.gate(D)
    H = W.holiday_week({s: k / n for s, (k, n, _) in since.items()})
    win = [x for x in D if x["day"] <= 146] + H
    assert U.naive(win, since=149)[0] == "GO"
    rows, dec, _ = U.gate(win, changes=[(149, "rc-1h", tuple(W.STRATA))], only=("G-1", "G-2", "G-3", "G-4"),
                          scorecard=False)
    assert dec == "HOLD"
    assert W.reweighted(W.by_stratum(H)) < 0.85 < W.agreement(H)[2]


def test_greystone_holds():
    G = W.greystone_window()
    letter = [x for x in G if x["cls"] == W.G_CLASSES[3]]
    assert len(letter) < 60
    hol = [x for x in G if x["day"] in W.G_HOLIDAY_DAYS]
    assert sum(x["agree"] for x in hol) / len(hol) >= 0.90


def test_clean_day_rule():
    assert U.clean_days(D, "rotated fax, no intake record", 150) == 4
    assert U.clean_days(D, "broker template, date received", 151) == 3
