"""Chapter 34 lab tests: the numbers the chapter quotes."""
import subprocess, sys, pathlib
import _paths  # noqa: F401
from extract import price, margin
from sl import caldwell_design
HERE = pathlib.Path(__file__).parent


def test_v0_misses_the_unmeasurable_level():
    _, _, _, lines = price("v3", honest=False, naive=True)
    assert round(margin(lines)[0] * 100, 1) == 17.9


def test_honest_v3_is_minus_eight():
    cs, _, _, lines = price("v3", honest=True)
    assert round(margin(lines)[0] * 100, 1) == -8.0
    assert sum(len(c.findings) for c in cs) == 8


def test_v5_is_clean_and_above_floor():
    cs, _, _, lines = price("v5", honest=True)
    assert sum(len(c.findings) for c in cs) == 0
    assert 0.40 < margin(lines)[0] < 0.60


def test_caldwell_design():
    d = caldwell_design()
    assert (d.n, d.k) == (310, 7)


def test_marcus_signed_version_clean():
    out = subprocess.run([sys.executable, "marcus.py"], cwd=HERE, capture_output=True, text=True).stdout
    assert out.count("findings: 0") == 1 and "UNDEFINED TRIGGER" in out
