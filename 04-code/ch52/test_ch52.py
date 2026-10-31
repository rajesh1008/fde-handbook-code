"""Chapter 52 lab tests: the numbers the chapter quotes."""
import subprocess, sys, pathlib, _paths  # noqa: F401
import world as W, suite as S
from absorb import WORK
from fieldkit.pyramid import MergeGate, caught_at
HERE = pathlib.Path(__file__).parent


def run(*a):
    return subprocess.run([sys.executable, *a], cwd=HERE, capture_output=True, text=True, check=True).stdout


def test_gold_split_and_fields():
    assert len(W.TEST_DOCS) == 201 and len(W.FIELDS) == 10 and len(W.DISPUTE_DOCS) == 34
    assert len(W.CAL_DOCS[1::2]) == 300


def test_deterministic_fields_do_not_move():
    b, a = W.scored(W.PIN), W.scored(W.N2)
    assert all(b[k] == a[k] for k in b if k[1] in W.DETERMINISTIC)


def test_rerun_numbers():
    out = run("rerun.py")
    assert "gm-n2              94.8%   93.6%      44     3         1   0.0051" in out
    assert "gm-n1: decision hold, caught at layer 2" in out and "gm-n2: decision block, caught at layer 2" in out
    assert "47/1823 = 2.6%" in out


def test_calibration_is_the_caught_change():
    res = S.pyramid().run({"version": W.N2, "signed_off": S.lost_critical(W.N2)}, stop_on_fail=False)
    assert MergeGate("Anne Kessler").decide(res)["decision"] == "block" and caught_at(res) == 3
    cal = S.calibrator(W.N2, W.CAL_DOCS[0::2])
    res = S.pyramid().run({"version": W.N2, "signed_off": S.lost_critical(W.N2), "calibrator": cal}, stop_on_fail=False)
    assert MergeGate("Anne Kessler").decide(res)["decision"] == "merge"


def test_summary_change_escapes_then_is_caught():
    out = run("escape.py")
    assert "gm-n2               22       12             131" in out
    assert "merge (4 of 4 checks pass" in out and "decision block, caught at layer 2" in out


def test_absorb_counts():
    assert len(WORK) == 30
    assert sum(w[3] == "FDE" for w in WORK) == 11 and sum(w[2] == "FDE" for w in WORK) == 22


def test_tryits():
    assert "with Anne Kessler's item-by-item sign-off: merge" in run("tryit.py", "a")
    assert "without the calibration layer: merge" in run("tryit.py", "b")
    assert "L3 inconclusive" in run("tryit.py", "c").splitlines()[1]
