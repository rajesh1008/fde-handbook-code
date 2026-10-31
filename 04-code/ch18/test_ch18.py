"""Chapter 18 lab checks: the numbers the chapter prints are the numbers this code produces."""
import subprocess, sys, pathlib
HERE = pathlib.Path(__file__).parent


def out(script, *args):
    return subprocess.run([sys.executable, str(HERE / script), *args], capture_output=True, text=True,
                          check=True).stdout


def test_sunday_rotation():
    s = out("sunday_rotation.py")
    assert "30 h 10 min" in s and "scored 177, missed 183" in s and "scored 356, missed 0, routed to a person 4" in s


def test_deprecation_register():
    s = out("deprecation.py")
    assert "48 days left" in s and "naive HTTP 410 endpoint_retired" in s and "level page" in s


def test_version_drift():
    s = out("version_drift.py")
    assert "day 77 Thu 00:00" in s and "gained 13, lost 7" in s


def test_framework_header_and_allowlist():
    assert "400 unsupported_parameter" in out("framework_header.py")
    s = out("allowlist.py")
    assert "denied requests 160; security alert raised" in s and "denied requests   1; no alert" in s


def test_greystone():
    s = out("greystone_capability.py")
    assert "embeddings MISSING" in s and "78/80 = 0.97" in s


def test_tryit():
    assert "unexpected share 0.3" in out("tryit.py", "c")
