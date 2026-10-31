"""Chapter 19 lab: the numbers the chapter prints are the numbers the code produces."""
import subprocess, sys, pathlib
HERE = pathlib.Path(__file__).parent


def out(s, *a):
    return subprocess.run([sys.executable, s, *a], cwd=HERE, capture_output=True, text=True, check=True).stdout


def test_failure_injection_shows_uat_pass_and_preprod_reject():
    o = out("writeback_failure.py")
    assert "uat      writes 152  accepted 152" in o and "preprod  writes 152  accepted 140" in o


def test_fixed_writeback_leaves_no_orphans_or_duplicates():
    o = out("writeback_fixed.py")
    assert "'SHELL'" not in o and "duplicate claims 0" in o


def test_end_to_end_zero_unexplained():
    assert "unexplained 0\nsupporting" in out("reconcile_caldwell.py")


def test_edi_parse_counts():
    assert "envelope errors 4, unknown codes 3, parsed 305" in out("pennant_edi.py")
