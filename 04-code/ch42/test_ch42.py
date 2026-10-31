"""Chapter 42 lab tests: the numbers the chapter quotes."""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
run = lambda *a: subprocess.run([sys.executable, *a], cwd=HERE, capture_output=True, text=True, check=True).stdout


def test_replay():
    v1, v0 = run("replay.py", "v1"), run("replay.py", "v0")
    assert "leading alarm day 20" in v1 and "threshold 0.80 -> 0.78" in v1 and "silently wrong documents in 90 days: 181" in v1
    assert "first alarm day 28" in v0 and "silently wrong documents in 90 days: 883" in v0
    assert "monitor running on day 90: no" in v0


def test_drill():
    v0, v2 = run("drill.py", "v0"), run("drill.py", "v2")
    assert "02:10  detect" in v0 and "time to mitigate 60 min" in v0
    assert "02:06  detect" in v2 and "time to mitigate 14 min" in v2


def test_deprecation():
    assert "EU lane documents to the clerks: 6164" in run("deprecation.py", "v0")
    v1 = run("deprecation.py", "v1")
    assert "PROMOTE" in v1 and "EU lane documents to the clerks: 0" in v1


def test_ownership_and_live_stable():
    o = run("ownership.py")
    for s in (" 0   0.40", " 14   0.30", " 70   0.80"):
        assert s in o
    assert "verdict: NOT YET" in run("livestable.py", "v0")
    assert "verdict: LIVE STABLE" in run("livestable.py", "v1")


def test_caldwell():
    assert "routing alarm in week 4" in run("caldwell.py")
