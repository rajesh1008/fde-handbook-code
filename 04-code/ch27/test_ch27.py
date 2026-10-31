"""Chapter 27 lab: every number the chapter prints, re-run."""
import common as C
import world as W
from fieldkit.routing import gate

aud = W.make("audit-400", 400)
R = C.route(aud)


def test_v0_fails_on_first_real_sample():
    iso, t, lb, n = C.v0()
    band = [i for i in C.gold() if iso.predict(i.verbal) >= t]
    assert t == 0.98 and lb >= 0.98
    assert round(sum(not i.right for i in band) / len(band), 3) == 0.148


def test_thresholds_signed_day_132():
    th = C.thresholds()
    assert (th.proceed, th.floor) == (0.95, 0.41) and th.lower_bound >= 0.98


def test_routing_shares():
    b = [d["band"] for d in R]
    assert (b.count("proceed"), b.count("review"), b.count("escalate")) == (249, 119, 32)


def test_post_review_error_36_of_4000():
    assert sum(not f["final"] for d in R for f in d["fields"]) == 36


def test_no_suggestion_below_floor():
    th = C.thresholds()
    for d in R:
        for f in d["fields"]:
            if C.model().score(f["item"]) < th.floor:
                assert not f["shown"]


def test_failed_gate_never_proceeds():
    for d in R:
        for f in d["fields"]:
            if gate(f["item"].ev):
                assert f["band"] != "proceed"
