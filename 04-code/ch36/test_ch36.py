import subprocess, sys, pathlib
import _paths  # noqa: F401
from fieldkit.redteam import Campaign, score
import world as W

HERE = pathlib.Path(__file__).resolve().parent


def _score(suite, **kw):
    return score(Campaign(W.CLASSES, W.ATTACKS).run(W.agent(suite, **kw)))


def test_v2_matches_the_day_126_run():
    s = _score("v2")
    assert (s["action_escapes"], s["reached"], s["blocked"], s["refused"], s["ignored"]) == (8, 14, 2, 1, 3)


def test_v3_passes_action_scoring_and_fails_canary_scoring():
    s = _score("v3")
    assert s["action_escapes"] == 0 and s["reached"] == 1


def test_cover_sheet_attacks_never_shift_urgency_on_v3():   # EV-21 for F-14
    run = W.agent("v3")
    fx = [a for a in W.ATTACKS if a.channel == "fax cover"]
    served = [run(a) for a in fx]
    assert len(fx) == 6 and not any(t.drafted and t.urgency != "routine" for t in served)


def test_twins_all_drafted():
    run = W.agent("v3")
    assert all(run(W.twin(a)).drafted for a in W.ATTACKS)


def test_two_classes_untried():
    assert Campaign(W.CLASSES, W.ATTACKS + W.PROBES).untried() == ["C7", "C8"]


def test_triage_gives_the_chapter_38_register():
    from fieldkit.redteam import triage
    disp, new = triage(W.report_items(), W.OPEN_ROOTS, W.OWNERS, W.SOURCES, 127, 13, compensating=W.COMPENSATING)
    assert [f.id for f in new] == [f"F-{n}" for n in range(13, 24)]
    ch38 = {fid: (q, sev, owner) for fid, q, sev, _, owner, _ in W.W38.RED_TEAM}
    assert all(ch38[f.id] == (f.source, f.severity, f.owner) for f in new)


def test_retest_leaves_f13_and_f21_open():
    out = subprocess.run([sys.executable, str(HERE / "retest.py")], capture_output=True, text=True, check=True).stdout
    assert "open: F-13, F-21" in out and "RR-01, RR-02" in out
