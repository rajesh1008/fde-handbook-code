"""Chapter 43 lab tests: the numbers the chapter quotes."""
import world as W
from fieldkit.handover import score
from fieldkit.service import two_year, summary, exit_lint, exit_drill


def _s(paths, key, start):
    p = paths[key]
    return summary(p, two_year(p, W.items(start)))


def test_start_states_match_chapters_41_and_42():
    assert score(W.items(W.PENNANT0)).gated == 0.8 and score(W.items(W.CALDWELL0)).gated == 0.9


def test_pennant_paths():
    h, m0, m = (_s(W.PENNANT_PATHS, k, W.PENNANT0) for k in ("hand-over", "managed-v0", "managed"))
    assert h[1]["customer"] == 187200 and m0[1]["customer"] == 240480 and m[1]["customer"] == 303600
    assert m0[1]["margin"] == 0.222 and m[1]["margin"] == 0.345 and m[2]["margin"] == 0.435
    assert m0[1]["readiness"] == 0.325 and m0[2]["readiness"] == 0.1 and m0[2]["takeover"] == 836
    assert m[1]["readiness"] == 0.8 and m[2]["readiness"] == 0.85


def test_caldwell_paths():
    c = _s(W.CALDWELL_PATHS, "hybrid", W.CALDWELL0)
    assert c[1]["readiness"] == 0.975 and c[1]["margin"] == 0.7 and c[1]["takeover"] == 52


def test_exit_lint_and_drill():
    assert sum(len(exit_lint(r, W.OWNERS)) for r in W.RB_V0) == 8
    assert sum(len(exit_lint(r, W.OWNERS)) for r in W.RB_V1) == 0
    d0 = exit_drill(W.RB_V0[0], W.OWNERS, "Nadia Brooks", W.DRILL_MINUTES, W.DRILL_WORKAROUND, 120, 210)
    d1 = exit_drill(W.RB_V1[0], W.OWNERS, "Nadia Brooks", W.DRILL_MINUTES, W.DRILL_WORKAROUND, 120, 210)
    assert (d0["passed"], d0["blocked_at"]) == (False, 2) and (d1["passed"], d1["end"]) == (True, 180)


def test_retainer_rollover():
    r = W.RET12
    assert r.fee == 4500 and r.margin(12) == 0.6 and r.margin(33, carried=21) == -0.1
