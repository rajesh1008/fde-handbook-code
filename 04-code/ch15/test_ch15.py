"""Chapter 15 lab tests: every pasted output must be reproducible."""
import subprocess, sys, pathlib
HERE = pathlib.Path(__file__).parent


def run(*a):
    return subprocess.run([sys.executable, *a], cwd=HERE, capture_output=True, text=True, check=True).stdout


def test_outputs_match_the_chapter():
    for f in sorted((HERE / "output").glob("*.txt")):
        stem = f.stem
        args = ["tryit.py", stem.split("_")[1]] if stem.startswith("tryit_") else [stem + ".py"]
        assert run(*args) == f.read_text(), stem


def test_failure_injection_refuses_the_delivery():
    out = run("failure_key_removed.py")
    assert "score=0.67  NOT READY" in out and "deletion proof by key" in out


def test_plumbing_check_separates_code_from_data():
    out = run("plumbing_check.py")
    assert "5 of 7" in out and "real 47 of 200" in out
